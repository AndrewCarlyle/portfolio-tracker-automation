import requests
import webbrowser
import subprocess
import time

from googleSheetsWriter import GoogleSheetsWriter

# The ID and range of a sample spreadsheet.
PORTFOLIO_SPREADSHEET_ID = '1M6ZNA_O1-T90ASBvttFo_hNroYqYCJKD_5SAjmBT1wg'
IBKR_CELL_NUM = 'Net Worth!B1'

GATEWAY_DIR_PATH = '/Users/andre/Workspace/clientportal.gw'

#Start the ibkr gateway server in order to auth with ibkr
def launchIbkrGateway():
    command = "bin/run.sh root/conf.yaml &"

    # Execute the command in the background
    subprocess.Popen(command, shell=True, cwd=GATEWAY_DIR_PATH)

    #Wait one second to allow the gateway to launch
    time.sleep(1)

def openLoginPage():
    loginUrl = 'https://localhost:8000'
    webbrowser.open(loginUrl)

def getAccountNums():
    url = "https://localhost:8000/v1/api/portfolio/accounts"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        accountNums = [act['id'] for act in response.json() ]
        print(f"Found accounts: {accountNums}")
        return accountNums
    else:
        print(f"Request failed with status code: {response.status_code}")

def getAccountCashValue(accountNum):
    url = f"https://localhost:8000/v1/api/portfolio/{accountNum}/ledger"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        print(f"Found {response.json()['BASE']['cashbalance']} in account {accountNum}")
        return response.json()['BASE']['cashbalance']
    else:
        print(f"Request failed with status code: {response.status_code}")

def main():
    launchIbkrGateway()

    openLoginPage()

    #Below steps will not work until the user is logged in
    input("Press Enter to continue once logged in...")

    accountNums = getAccountNums()

    cashTotal = 0

    for account in accountNums:
        cashTotal += getAccountCashValue(account)

    print(f"Total cash balance: {cashTotal}")

    writer = GoogleSheetsWriter()
    writer.writeValueToSheet(PORTFOLIO_SPREADSHEET_ID, IBKR_CELL_NUM, [str(cashTotal)])

if __name__ == '__main__':
    main()
