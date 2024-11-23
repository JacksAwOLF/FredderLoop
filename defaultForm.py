from datetime import datetime


def getDefaultFormHead():
    date = datetime.today().strftime("%Y-%m-%d")
    return {"info": {"title": date + " LetterLoop Questions", "documentTitle": date}}


# https://googleapis.github.io/google-api-python-client/docs/dyn/forms_v1.html
defaultFormBody = {
    "requests": [
        {
            "updateFormInfo": {
                "info": {
                    "description": "Google Forms API is extremely limited so "
                    + "please double check that 'Collect Email Addresses' is Verified, "
                    + "'Allow Response Editing' and 'Limit to 1 Response' is turned on in "
                    + "Settings -> Responses ;)"
                },
                "updateMask": "description",
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "What is your name?",
                    "description": "",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {"paragraph": False},
                        }
                    },
                },
                "location": {"index": 0},
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Alright! Here's a letter loop question",
                    "description": "",
                    "questionItem": {"question": {"textQuestion": {"paragraph": True}}},
                },
                "location": {"index": 1},
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Photo Wall",
                    "description": "Be sure to update this to collect photos! "
                    + "TODO: make it do this automatically",
                    "questionItem": {"question": {"textQuestion": {"paragraph": True}}},
                },
                "location": {"index": 2},
            }
        },
    ]
}
