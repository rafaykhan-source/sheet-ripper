import logging
import os.path
from dataclasses import dataclass, field

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@dataclass
class SheetService:
    scopes: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        self.logger = logging.getLogger(__name__)

    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
            self.logger.debug("Retrieved credentials from token.json")

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                self.logger.debug("Retrieved credentials from token.json")

        return creds

    def build_sheets(self):
        creds = self._authenticate()
        with build("sheets", "v4", credentials=creds) as service:
            self.sheets = service.spreadsheets()

    def get_sheet_values(self, id: str, range: str):
        try:
            result = (
                self.sheets.values()
                .get(
                    spreadsheetId=id,
                    range=range,
                )
                .execute()
            )
            data = result.get("values", [])
            if not data:
                self.logger.error("Failed to retrieve data.")
                return
            self.logger.info("Retrieved data: %s", data[0])
            return data

        except HttpError as err:
            print(err)
