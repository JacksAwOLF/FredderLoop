import datetime

import constants
import docUtil
from services import create_service


def _get_questions(form: dict) -> dict:
    questions = {}
    for question in form["items"]:
        questions[question["questionItem"]["question"]["questionId"]] = question[
            "title"
        ]
    return questions


# https://googleapis.github.io/google-api-python-client/docs/dyn/forms_v1.html
def _process_responses(form: dict, responses: dict) -> tuple[dict, dict]:
    questions = _get_questions(form)
    processed = {}
    email_mapping = {}

    counter = 0
    # get only questions and responses
    for response in responses: #["responses"]:
        if response.get("respondentEmail"):
            user_email = response["respondentEmail"]
        else:
            user_email = f"N/A-{counter}"
            counter += 1
        for questionId, answer in response["answers"].items():
            question_text = questions[questionId]
            for k, v in answer.items():
                if "answer" in k.lower():
                    answer_block = v["answers"]
                    if not processed.get(question_text):
                        processed[question_text] = {}
                    if not processed[question_text].get(user_email):
                        processed[question_text][user_email] = []

                    # Save mapping between email and name
                    if "What is your name?" == question_text:
                        email_mapping[user_email] = answer_block[0]["value"]

                    for ans in answer_block:
                        # differentiate between photo and text response
                        if "value" in ans.keys():
                            processed[question_text][user_email].append(ans["value"])
                        elif "fileId" in ans.keys():
                            processed[question_text][user_email].append(ans["fileId"])
                        else:
                            print(f"ERROR: Unknown answer types {answer_block.keys()}")
                    break

    final_processed = []
    for question, answers in processed.items():
        # don't include name as a question
        if "What is your name?" == question:
            continue
        temp = {}
        for user, answer in answers.items():
            temp[email_mapping[user]] = answer
        final_processed.append({question: temp})

    # catch if photo wall not at end, move it to the end
    if "photo wall" not in list(final_processed[-1].keys())[0].lower():
        ind = 0
        for q_a in final_processed:
            question = list(q_a.keys())[0]
            if "photo wall" in question.lower():
                final_processed.append({question: q_a[question]})
                del final_processed[ind]
                break
            ind += 1

    return final_processed, email_mapping


def createNewsletter(form: dict, responses: dict) -> tuple[str, dict]:
    docs_service = create_service(constants.DOCS_SERVICE)

    doc = docUtil.create_document(
        docs_service=docs_service,
        title=f"{datetime.datetime.now().strftime('%Y-%m')} Gletterloop Newsletter",
    )
    doc_id = doc["documentId"]
    current_index = 1
    processed, email_mapping = _process_responses(form, responses)
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

    # update font
    tmp, _ = docUtil.update_font(curr_ind=current_index)
    requests.extend(tmp)

    # push changes
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()

    return doc_id, email_mapping
