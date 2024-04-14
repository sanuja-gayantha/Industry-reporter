# Developed by @sanuja : https://github.com/sanuja-gayantha

import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .constants import GOOGLE_SHEET_SCOPES, SPREADSHEET_ID


class Sheet_Api():
    def __init__(self):
        self.credentials = None
        self.SCOPES = [GOOGLE_SHEET_SCOPES]
        self.authentication()


    def authentication(self):
        if os.path.exists("./api/google_sheet/token.json"):
            self.credentials = Credentials.from_authorized_user_file("./api/google_sheet/token.json", self.SCOPES)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./api/google_sheet/credentials.json", self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("./api/google_sheet/token.json", "w") as token:
                    token.write(self.credentials.to_json())


    def api_read_spreadsheet(self):
        try:
            service = build("sheets", "v4", credentials=self.credentials)
            result = (
                service.spreadsheets().values()
                .get(spreadsheetId=SPREADSHEET_ID, range="Details!A2:F59997")
                .execute())
            
            values = result.get("values", [])

            temp_pdf_links=[]
            for row in values:
                temp_pdf_links.append(row[3])
            return temp_pdf_links
  
        except HttpError as err:
            print(err)
    

    def api_append_spreadsheet(self, values):
        try:
            service = build("sheets", "v4", credentials=self.credentials)
            body = {"values": [values]}
            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=SPREADSHEET_ID,
                    range="Details!A2:F59997",
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended...")
            return result

        except HttpError as err:
            print(err)
    















