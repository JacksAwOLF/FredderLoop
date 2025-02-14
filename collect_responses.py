"""Start collecting responses"""

import sys

from src.utils import database, discord, drive, services

if __name__ == "__main__":
    docs_service = services.create_docs_service()
    drive_service = services.create_drive_service()

    form_id = database.get_form_id(docs_service=docs_service)
    if form_id == "":
        sys.exit()

    # remove all permissions (other than owning the file itself)
    drive.remove_all_permissions(drive_service=drive_service, file_id=form_id)

    # add permission to view the files to anyone for submission
    drive.add_anyone_read(drive_service=drive_service, file_id=form_id)

    discord.collect_responses_message()
