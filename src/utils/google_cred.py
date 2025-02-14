"""Module to set up Google Console authentication"""

import google.oauth2 as oauth

from src import config

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

credentials = oauth.service_account.Credentials.from_service_account_file(
    config.SERVICE_ACCOUNT_CREDENTIALS_FILE, scopes=SCOPES
)
