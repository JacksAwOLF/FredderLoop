Building:

Every push to main will update the crontab code on the Ubuntu server
the cronjobs to run are in the file cronjobs

Architecture Proposal:

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
