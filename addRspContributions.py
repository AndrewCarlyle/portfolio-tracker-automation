from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
PORTFOLIO_SPREADSHEET_ID = '14MXCb90sj_Ic_lYDU1ibYEQ0YBaQOuBt-bEO0hn7za8'
#SAMPLE_RANGE_NAME = 'RSP Contributions!D2:D'
SAMPLE_RANGE_NAME = 'Sheet5!A1:B1'

class contributionAutomation:

    def __init__(self):
        self.creds = None
        self.authenticate()

        self.service = build('sheets', 'v4', credentials=self.creds)

        self.date = getDate()

    def getLastEntryIndex(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=PORTFOLIO_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            print('Result:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s' % (row[0]))
        except HttpError as err:
            print(err)
    
    def writeValueToSheet(self, amount):
        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().append(spreadsheetId=PORTFOLIO_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body=dict(
                majorDimension="ROWS",
                values=[
                    [amount, amount]
                ])).execute()
            print(result)
            values = result.get('values', [])

        except HttpError as err:
            print(err)

    def authenticate(self):
        # The file token.json stores the user's access and refresh tokens, and is created automatically 
        # when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

def getDate():
    return -1

def main():
    contrAutomation = contributionAutomation()
    contrAutomation.writeValueToSheet(163.46)

if __name__ == '__main__':
    main()