import datetime

import constants
import database
import docUtil
import formUtil
from services import create_service


def createNewsletter(form: dict, responses: dict) -> tuple[str, dict]:
    docs_service = create_service(constants.DOCS_SERVICE)

    doc = docUtil.create_document(
        docs_service=docs_service,
        title=f"{datetime.datetime.now().strftime('%Y-%m')} Gletterloop Newsletter",
    )
    doc_id = doc["documentId"]
    # save newsletter ID
    database.pushToDatabase(docs_service=docs_service, content=f"newsletterID:{doc_id}")
    current_index = 1
    processed, email_mapping = formUtil.process_responses(form, responses)
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
    docUtil.batch_update(docs_service=docs_service, file_id=doc_id, requests=requests)

    return doc_id, email_mapping
