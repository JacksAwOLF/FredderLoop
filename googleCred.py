from config import SERVICE_ACCOUNT_CREDENTIALS_FILE
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_CREDENTIALS_FILE, scopes=SCOPES
)
