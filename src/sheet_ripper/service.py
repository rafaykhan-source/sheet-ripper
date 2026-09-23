import logging
import os.path
from dataclasses import dataclass, field

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sheet_ripper.utilities import get_config_path


@dataclass
class SheetService:
    scopes: list[str] = field(default_factory=list)
    "The desired scopes of the sheet service."
    auth_path: str | None = None
    "The relative path to the credentials.json and token.json files."

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.auth_path:
            self.auth_path = get_config_path()
        if not self.scopes:
            self.scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        self._build_sheets()

    def _write_token(self, creds: Credentials) -> None:
        with open(f"{self.auth_path}/token.json", "w") as token:
            token.write(creds.to_json())
            self.logger.debug("Wrote credentials to token.json")

    def _get_creds_from_token(self) -> Credentials:
        if os.path.exists(f"{self.auth_path}/token.json"):
            creds = Credentials.from_authorized_user_file(
                f"{self.auth_path}/token.json",
                self.scopes,
            )
            self.logger.debug("Retrieved credentials from token.json")

        return creds

    def _get_creds_from_auth_flow(self) -> Credentials:
        auth_flow = InstalledAppFlow.from_client_secrets_file(
            f"{self.auth_path}/credentials.json",
            self.scopes,
        )
        creds = auth_flow.run_local_server(port=0)
        self.logger.debug("Retrieved credentials from authentication flow.")

        return creds

    def _authenticate(self) -> Credentials:
        """Returns user credentials for authentication.

        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        Returns:
            Credentials: The user credentials for authentication.
        """
        creds_from_token = self._get_creds_from_token()

        if not creds_from_token:
            creds = self._get_creds_from_auth_flow()
            self._write_token(creds)
            return creds

        if creds_from_token.expired and creds_from_token.refresh_token:
            creds_from_token.refresh(Request())
            return creds_from_token

        creds = self._get_creds_from_auth_flow()
        self._write_token(creds)

        return creds

    def _build_sheets(self):
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
