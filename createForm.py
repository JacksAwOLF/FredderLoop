from apiclient import discovery

from googleCred import credentials
from defaultForm import getDefaultFormHead, defaultFormBody
from discordBot import createFormMessage
from database import saveFormId
from config import GOOGLE_DRIVE_FOLDER_ID


if __name__ == "__main__":
    form_service = discovery.build("forms", "v1", credentials=credentials)
    drive_service = discovery.build('drive', 'v3', credentials=credentials)

    # create the form
    form = form_service.forms().create(
        body=getDefaultFormHead()
    ).execute()
    formId = form['formId']

    # add default questions
    form_service.forms().batchUpdate(
        formId=formId,
        body=defaultFormBody
    ).execute()

    # set form editing permissions to anyone with the link
    drive_service.permissions().create(
        fileId=formId,
        body={
            'type': 'anyone',
            'role': 'writer',
        }
    ).execute()

    # Move the form to specific folderId
    prevParents = ",".join(drive_service.files().get(
        fileId=formId,
        fields='parents'
    ).execute()['parents'])

    file = drive_service.files().update(
        fileId=formId,
        addParents=GOOGLE_DRIVE_FOLDER_ID,
        removeParents=prevParents,
        fields='id, parents'
    ).execute()

    # save formId in database
    print("form created: ", form)
    saveFormId(form['formId'])

    createFormMessage()
