# Developed by @sanuja : https://github.com/sanuja-gayantha

import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .constants import SCOPES, SPREADSHEET_ID


class Api():
    def __init__(self):
        self.credentials = None
        self.SCOPES = [SCOPES]
        self.authentication()


    def authentication(self):
        if os.path.exists("./api/token.json"):
            self.credentials = Credentials.from_authorized_user_file("./api/token.json", self.SCOPES)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./api/credentials.json", self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("./api/token.json", "w") as token:
                    token.write(self.credentials.to_json())


    def api_read_spreadsheet(self):
        try:
            service = build("sheets", "v4", credentials=self.credentials)
            sheet = service.spreadsheets()

            result = (
                sheet.values()
                .get(spreadsheetId=SPREADSHEET_ID, range="Details!A2:E")
                .execute())
            
            values = result.get("values", [])
            temp_pdf_links=[]
            for row in values:
                temp_pdf_links.append(row[3])
            return temp_pdf_links
  
        except HttpError as err:
            print(err)
    

    def api_append_spreadsheet(self):
















