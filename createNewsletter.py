import datetime
import copy

from temp import response as r
from form import form as f
import constants as c
import services as svc
import editNewsletter as docUtil


def get_form():
    return f


def get_response():
    return r


def get_questions(form) -> dict:
    # form_title = form["info"]["documentTitle"]
    questions = {}
    for question in form["items"]:
        questions[question["questionItem"]["question"]["questionId"]] = question[
            "title"
        ]
    return questions


# https://googleapis.github.io/google-api-python-client/docs/dyn/forms_v1.html
def process_responses(form, responses):
    questions = get_questions(form)
    # print(questions)
    processed = {}
    email_mapping = {}
    for response in responses["responses"]:
        user_email = response["respondentEmail"]
        for questionId, answer in response["answers"].items():
            question_text = questions[questionId]
            for k, v in answer.items():
                if "answer" in k.lower():
                    answer_block = v["answers"]
                    if not processed.get(question_text):
                        processed[question_text] = {}
                    if not processed[question_text].get(user_email):
                        processed[question_text][user_email] = []

                    if "What is your name?" == question_text:
                        email_mapping[user_email] = answer_block[0]["value"]

                    for ans in answer_block:
                        if "value" in ans.keys():
                            processed[question_text][user_email].append(ans["value"])
                        elif "fileId" in ans.keys():
                            processed[question_text][user_email].append(ans["fileId"])
                        else:
                            print(f"ERROR: Unknown answer types {answer_block.keys()}")
                    break
    final_processed = []
    for question, answers in processed.items():
        if "What is your name?" == question:
            continue
        temp = {}
        for user, answer in answers.items():
            temp[email_mapping[user]] = answer
        # if "photo wall" in question.lower():
        #     final_processed.insert(0, {question: temp})
        # else:
        final_processed.append({question: temp})
    if "photo wall" not in list(final_processed[-1].keys())[0].lower():
        ind = 0
        for q_a in final_processed:
            question = list(q_a.keys())[0]
            if "photo wall" in question.lower():
                final_processed.append({question: q_a[question]})
                del final_processed[ind]
                break
            ind += 1
        
    # final_processed.reverse()
    # print(processed)
    # print(final_processed)
    return final_processed


# https://developers.google.com/docs/api/reference/rest
# https://googleapis.github.io/google-api-python-client/docs/dyn/docs_v1.documents.html
def create_document(docs_service, title: str) -> str:
    body = {"title": title}
    print(docs_service.documents().create(body=body).execute())


def share_document(drive_service, doc_id: str, emails: list) -> None:
    if type(emails) != list:
        raise TypeError(f"incorrect emails type: {type(emails)}")
    for email in emails:
        print(f"adding: {email}")
        drive_service.permissions().create(
            fileId=doc_id,
            body={"type": "user", "emailAddress": email, "role": c.WRITER_PERMISSION},
        ).execute()
        print(f"added writer role for: {email}")


# https://developers.google.com/drive/api/guides/manage-sharing#python
def transfer_ownership(
    drive_service, doc_id: str, permission_id: str, email: str
) -> None:
    # https://issuetracker.google.com/issues/228791253
    print(
        "Currently Drive does not support changing the ownership for items which are owned by gmail.com accounts; it's supported for Workspace accounts."
    )


def get_permissions(drive_service, doc_id: str) -> str:
    permissions = (
        drive_service.permissions().list(fileId=doc_id).execute()["permissions"]
    )
    print(permissions)
    for perm in permissions:
        if perm["role"] == c.WRITER_PERMISSION:
            return perm["id"]

    raise Exception(f"unknown permissions: {str(permissions)}")


def trash_document(drive_service, doc_id: str):
    print(f"Trashing document: {doc_id}")
    body = {"trashed": True}
    drive_service.files().update(fileId=doc_id, body=body).execute()


def untrash_file(drive_service, file_id: str):
    print(f"Attempting to untrash file: {file_id}")
    body = {"trashed": False}
    drive_service.files().update(fileId=file_id, body=body).execute()


def add_anyone_write(drive_service, file_id: str):
    print(f"Adding anyoneWithLink can write permission: {file_id}")
    body = {
        "type": "anyone",
        "role": "writer",
        "allowFileDiscovery": False,
    }
    drive_service.permissions().create(fileId=file_id, body=body).execute()


def createNewsletter(form, responses) -> str:
    # docs documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/docs_v1.documents.html
    # services = (
    #     svc.Services().create_service(c.DRIVE_SERVICE).create_service(c.DOCS_SERVICE)
    # )
    drive_service = svc.create_service(c.DRIVE_SERVICE)
    docs_service = svc.create_service(c.DOCS_SERVICE)

    # doc = create_document(
    #     docs_service=docs_service,
    #     title="test document",
    # )
    doc_id = ""
    current_index = (
        docs_service.documents()
        .get(documentId=doc_id, fields="body")
        .execute()
        .get("body")
        .get("content")[-1]
        .get("endIndex")
    )
    if current_index == 2:
        current_index = 1
    processed = process_responses(form, responses)
    requests = []

    # add title
    title = f"Gletterloop for {datetime.datetime.now().strftime('%B %Y')}"
    tmp, current_index = docUtil.add_title(title, current_index)
    requests.extend(tmp)

    # add horizontal bar (with thin table with top border line cuz no horizontal rule w/ google docs api)
    tmp, current_index = docUtil.add_horizontal_rule(current_index)
    requests.extend(tmp)

    photo_ans = processed.pop()
    # add each question besides photo (pop photo into diff var)
    for response in processed:
        tmp, current_index = docUtil.add_response(response, current_index)
        requests.extend(tmp)

    # add photos
    tmp, current_index = docUtil.add_photos(photo_ans, current_index)
    requests.extend(tmp)
    # print(photo_ans)

    # update font
    tmp, _ = docUtil.update_font(curr_ind=current_index)
    requests.extend(tmp)

    # submit changes
    # print()
    # print()
    # print()
    # ind = 0
    # with open("temp3.py", "w+") as tmp_f:
    #     with open("temp4.py", "w+") as tmp_f2:
    #         # requests = requests[0:29]
    #         tmp_f.write("{")
    #         for request in requests:
    #             req = copy.deepcopy(request)
    #             req["ind"] = ind
    #             ind += 1
    #             tmp_f.write(str(req))
    #             tmp_f.write(",")
    #         tmp_f.write("}")
    #         docs_service.documents().batchUpdate(
    #             documentId=doc_id, body={"requests": requests}
    #         ).execute()
    #         tmp_f2.write(
    #             str(
    #                 docs_service.documents()
    #                 .get(documentId=doc_id)
    #                 .execute()
    #                 .get("body")
    #                 .get("content")
    #             )
    #         )

    docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()


createNewsletter(get_form(), get_response())
