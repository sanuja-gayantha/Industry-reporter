# Developed by @sanuja : https://github.com/sanuja-gayantha

import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .constants import SPREADSHEET_ID


# class Api():
#     def __init__(self):
#         self.pdf_data_list_path = os.path.join(os.getcwd(), 'pdfDataList.json')
    
#     def read_json_file(self, path):
#         with open(path) as json_file:
#             result = json.load(json_file)
#             return result

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def api_main():
    # pdf_data_list_path = os.path.join(os.getcwd(), 'pdfDataList.json')

    # ins = Api()
    # print(ins.read_json_file(pdf_data_list_path))

    credentials = None
    if os.path.exists("./api/token.json"):
        credentials = Credentials.from_authorized_user_file("./api/token.json", SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./api/credentials.json", SCOPES
            )
            credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("./api/token.json", "w") as token:
                token.write(credentials.to_json())


    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range="Details!A2:E")
            .execute())
        
        values = result.get("values", [])

        for row in values:
            print(row)
        # Print columns A and E, which correspond to indices 0 and 4.
        # print(f"{row[0]}, {row[4]}")


    except HttpError as err:
        print(err)









