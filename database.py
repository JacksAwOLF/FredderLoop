# import os
import traceback

import config
import docUtil
import masker

databaseDir = "./database"
formIdDir = databaseDir + "/formId"


def initDatabase():
    masker.log("Not running on-prem, no need to initDatabase")
    pass
    # if not os.path.isdir("./database"):
    #     os.mkdir(databaseDir)


def saveFormId(docs_service, formId):
    return pushToDatabase(docs_service=docs_service, content=f"formID:{formId}")
    # initDatabase()
    # with open(formIdDir, "w") as f:
    #     f.write(formId)


def pushToDatabase(docs_service, content):
    insert_index = docUtil.get_last_insert_index(
        docs_service=docs_service, file_id=config.DOC_ID_DOCUMENT_ID
    )
    request, curr_index = docUtil.add_paragraph(content, insert_index)
    err = docUtil.batch_update(docs_service, config.DOC_ID_DOCUMENT_ID, request)
    if not err:
        masker.log(
            " ".join(
                map(str, traceback.format_exception(type(err), err, err.__traceback__))
            )
        )
    # initDatabase()
    # with open(formIdDir, "w") as f:
    #     f.write(formId)


def getFormId(docs_service):
    return (
        docUtil.search_latest_text_lower(
            docs_service=docs_service,
            file_id=config.DOC_ID_DOCUMENT_ID,
            search_string="formID",
        )
        .split(":")
        .strip()
    )
    # initDatabase()
    # with open(formIdDir, "r") as f:
    #     return f.read().strip()
