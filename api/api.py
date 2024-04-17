# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from .constants import SPREADSHEET_ID, GOOGLE_SHEET_SCOPES, GOOGLE_DRIVE_SCOPES

class Api():
    def __init__(self, api_scope):
        self.credentials = None
        self.SCOPES = [api_scope]
        self.authentication()


    def authentication(self):
        path=""
        if self.SCOPES == [GOOGLE_SHEET_SCOPES]:
            path = "./api/spreadsheets/"
        elif self.SCOPES == [GOOGLE_DRIVE_SCOPES]:
            path = "./api/drive/"

        if os.path.exists(f"{path}/token.json"):
            self.credentials = Credentials.from_authorized_user_file(f"{path}/token.json", self.SCOPES)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{path}/credentials.json", self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(f"{path}/token.json", "w") as token:
                    token.write(self.credentials.to_json())

    # Call the Sheet Activity API
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
            print(f"{(result.get('updates').get('updatedCells'))} cells appended to google sheet...")
            return result

        except HttpError as err:
            print(err)
    

    # Call the Drive Activity API
    def api_upload_to_drive(self, pdf_file_path, pdf_file_title):
        try:
            # create drive api client
            service = build("drive", "v3", credentials=self.credentials)

            response = service.files().list(
                q="name='Industry_reporter' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive'
            ).execute()

            if not response['files']:
                folder_metadata = {
                    "name": "Industry_reporter",
                    "mimeType": "application/vnd.google-apps.folder",
                }
                file = (
                    service.files()
                    .create(body=folder_metadata, fields="id")
                    .execute()
                )
                folder_id=file.get('id')

            else:
                folder_id=response['files'][0]['id']


            file_metadata = {
                    "name": f"{pdf_file_title}",
                    "parents": [folder_id],
                }
            media = MediaFileUpload(f"{pdf_file_path}", resumable=True) 
            pdf_file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="webViewLink,id")
                .execute()
            )
            print(f'File ID: {pdf_file.get("id")} uploaded to drive...')
            print(f'{pdf_file.get("webViewLink")} is the drive link...')

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None
            pdf_file = None

        return pdf_file.get("webViewLink")
      













