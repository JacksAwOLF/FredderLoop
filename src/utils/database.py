"""Module containing database utility functions"""

# import os
import traceback

from src import config
from src.utils import docs, masker


def save_form_id(docs_service, form_id):
    """Save form id to specified document 'database'"""
    return push_to_database(docs_service=docs_service, content=f"form_id:{form_id}")


def push_to_database(docs_service, content):
    """Helper function appending to specified document 'database'"""
    insert_index = docs.get_last_insert_index(
        docs_service=docs_service, file_id=config.DOC_ID_DOCUMENT_ID
    )
    request, _ = docs.add_paragraph(content, insert_index)
    err = docs.batch_update(docs_service, config.DOC_ID_DOCUMENT_ID, request)
    if err:
        masker.log(
            " ".join(
                map(str, traceback.format_exception(type(err), err, err.__traceback__))
            )
        )


def get_form_id(docs_service):
    """Helper function pulling last form id from specified document 'database'"""
    form_id = (
        docs.search_latest_text_lower(
            docs_service=docs_service,
            file_id=config.DOC_ID_DOCUMENT_ID,
            search_string="form_id",
        )
        .split(":")[-1]
        .strip()
    )
    if "" == form_id:
        raise KeyError("form id not found in database")
    return form_id
