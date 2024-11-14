# FredderLoop
FredderLoop is a free alternative to LetterLoop which is only free for the first two issues. FredderLoop helps individuals update each other in monthly issues with all the spicy tea and pics from the previous month.

## Building:

Every push to main will update the crontab code on the Ubuntu server
the cronjobs to run are in the file cronjobs

## Architecture Proposal:

schedule python scripts to run periodically with crontab -e on ubuntu server

(github stores the crontab file that schedules the scripts and the various scripts to run)
(setup ubuntu server to listen to github actions to update code and run crontabs)
(set up google service account to create and manage forms so that users cannot edit / view them easily)

createForm.py
- runs at the beginning of every month
- creates a google form with a sharable link in a specified folder
- toggle setting to allow users to edit their responses after submitting (currently not supported)
- set permissions so that everyone with the link can edit the google form
- boot up discord bot to share link for form in letter loop channel

collectResponses.py
- runs 3 weeks after form is created, monthly
- changes permission so that form is not editable
- boot up discord bot to notify channel to submit responses

shareResponses.py
- runs 4 weeks after form is created, monthly
- several options here
    - creates a google doc with all the responses
    - creates and hosts a website with all the responses
    - (doing this) doesn’t do anything really just share the google form response link
- have to make sure pictures are nicely displayed
- would be nice to be able to comment and sort responses by question / person
- boot up discord bot to notify responses are available

(optional)
reminders.py
- runs a day before shareResponses run
- boot up discord bot to remind people who haven’t submitted
- this means bot will have to maintain a set of people who are in letterloop and a set of people who have submitted the form
- this could mean maybe give bot access to user and roles in the server
- this could mean have a field in form to specify discord username or email


helper files:

database.py and database
- stores the formId of the created google form for ease of access

googleCred.py
- returns the google credentials

defaultForm.py
- contains default questions to populate the FredderLoop

discordBot.py
- has a function to send a single message to discord server

## Local Development:

### Requirements:

* python3 >= 3.10.7
* pip
* python3.10-venv
* Google Cloud project
* Google credentials
* Google service account

### Setting up the Google Cloud project/credentials

This [python quickstart guide](https://developers.google.com/forms/api/quickstart/python) can be used as a reference for most of the steps. Deviations or additional steps are noted below

#### API Scopes

Below are the required API scopes for this project.

* Google Forms API - Used to interact with Google Forms
* Google Drive API - `https://www.googleapis.com/auth/drive.file`, Create new Drive files, or modify existing files, that you open with an app or that the user shares with an app while using the Google Picker API or the app's file picker.

### config.py:

`config.py` should be used to store credentials, but should NEVER be pushed with production secrets.

**Note**: The credentials and tokens do not need to be generated to modify a current setup and instructions are present for creating your own setup.

```
SERVICE_ACCOUNT_CREDENTIALS=<name of json file containing service account key>
GOOGLE_DRIVE_FOLDER_ID=<last segment of google drive folder url (after last "/")>
DISCORD_LETTERLOOP_CHANNEL_ID=<last segment of discord channel in browser version (after last "/")>
BOT_TOKEN=<from discord bot>
```

### SERVICE_ACCOUNT_CREDENTIALS

Follow the Google Forms quickstart guide and you can download this json file after adding a key to the service account.

### local environment

Use the following to create and start a virtual environment with the required python libraries installed.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Note**: Use `deactivate` to exit out of the virtual environment
