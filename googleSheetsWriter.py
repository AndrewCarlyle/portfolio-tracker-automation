import os.path
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#Path to directory where the .json files are stored
CREDENTIAL_DIR_PATH = '/Users/andre/Workspace/portfolio-tracker-automation'

class GoogleSheetsWriter:
    def __init__(self):
        self.creds = None
        self.authenticate()

        self.service = build('sheets', 'v4', credentials=self.creds)
    
    #spreadsheet string the ID of the spreadsheet eg. '1M6ZNA_O1-T90ASBvttFo_hNroYqYCJKD_5SAjmBT1wg'
    #cellrange string eg. 'Net Worth!B1'
    #values list of value to write to the spreadsheet at cellRange
    def writeValueToSheet(self, spreadsheet, cellRange, values):
        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().update(spreadsheetId=spreadsheet, range=cellRange, valueInputOption='USER_ENTERED', body=dict(
                majorDimension="ROWS",
                values=values)
            ).execute()
            
            print(f"Update result:{result}")

        except HttpError as err:
            print(err)

    #spreadsheet string the ID of the spreadsheet eg. '1M6ZNA_O1-T90ASBvttFo_hNroYqYCJKD_5SAjmBT1wg'
    #cellrange string eg. 'Net Worth!B1'
    #values list of value to write to the spreadsheet at cellRange
    def appendValueToSheet(self, spreadsheet, cellRange, values):
        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().append(spreadsheetId=spreadsheet, range=cellRange, valueInputOption='USER_ENTERED', body=dict(
                majorDimension="ROWS",
                values=[values])
            ).execute()
            
            print(f"Update result:{result}")

        except HttpError as err:
            print(err)

    def authenticate(self):
        def browserLogin():
            flow = InstalledAppFlow.from_client_secrets_file(f'{CREDENTIAL_DIR_PATH}/credentials.json', SCOPES)
            self.creds = flow.run_local_server(port=0)

        # The file token.json stores the user's access and refresh tokens, and is created automatically 
        # when the authorization flow completes for the first time.
        if os.path.exists(f'{CREDENTIAL_DIR_PATH}/token.json'):
            self.creds = Credentials.from_authorized_user_file(f'{CREDENTIAL_DIR_PATH}/token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except RefreshError as e:
                    #Delete existing expired token and re-attempt authentication
                    command = 'rm -f token.json'
                    subprocess.run(command, shell=True)

                    browserLogin()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{CREDENTIAL_DIR_PATH}/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(f'{CREDENTIAL_DIR_PATH}/token.json', 'w') as token:
                token.write(self.creds.to_json())
