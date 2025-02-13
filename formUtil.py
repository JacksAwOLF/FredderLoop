# https://googleapis.github.io/google-api-python-client/docs/dyn/forms_v1.html
import masker
from defaultForm import getDefaultFormHead, defaultFormBody


def create_form(form_service) -> any:
    return form_service.forms().create(body=getDefaultFormHead()).execute()


def add_default_form_body(form_service, form_id: str) -> None:
    form_service.forms().batchUpdate(formId=form_id, body=defaultFormBody).execute()


def get_form(form_service, form_id: str) -> any:
    return form_service.forms().get(formId=form_id).execute()


def get_form_responses(form_service, form_id: str) -> any:
    return form_service.forms().responses().list(formId=form_id).execute()


def get_questions(form: dict) -> dict:
    questions = {}
    for question in form["items"]:
        questions[question["questionItem"]["question"]["questionId"]] = question[
            "title"
        ]
    return questions


def get_response_names(form: dict, responses: dict) -> tuple[dict, list]:
    pass


def process_responses(form: dict, responses: dict) -> tuple[dict, dict]:
    questions = get_questions(form)
    processed = {}
    email_mapping = {}

    counter = 0
    # get only questions and responses
    for response in responses:  # ["responses"]:
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
                            masker.log(f"ERROR: Unknown answer types {answer_block.keys()}")
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
