import subprocess
import requests
import time
import webbrowser

class IbkrCash:
    def __init__(self, gatewayDir='/Users/andre/Workspace/clientportal.gw'):
        self.gatewayDir = gatewayDir
        self.portalProcess = self.launchIbkrGateway()

        self.openLoginPage()

    #Start the ibkr gateway server in order to auth with ibkr
    def launchIbkrGateway(self):
        command = "bin/run.sh root/conf.yaml &"

        # Execute the command in the background
        process = subprocess.Popen(command, shell=True, cwd=self.gatewayDir)

        #Wait one second to allow the gateway to launch
        time.sleep(1)

        return process

    def openLoginPage(self):
        loginUrl = 'https://localhost:8000'
        webbrowser.open(loginUrl)

    def getAccountNums(self):
        url = "https://localhost:8000/v1/api/portfolio/accounts"

        response = requests.get(url, verify=False)

        if response.status_code == 200:
            accountNums = [act['id'] for act in response.json() ]
            print(f"Found accounts: {accountNums}")
            return accountNums
        else:
            print(f"Request failed with status code: {response.status_code}")

    def getAccountCashValue(self, accountNum):
        url = f"https://localhost:8000/v1/api/portfolio/{accountNum}/ledger"

        response = requests.get(url, verify=False)

        if response.status_code == 200:
            print(f"Found {response.json()['BASE']['cashbalance']} in account {accountNum}")
            return response.json()['BASE']['cashbalance']
        else:
            print(f"Request failed with status code: {response.status_code}")

    def endPortalProcess(self):
        subprocessIdentifier = "/usr/bin/java -server -Dvertx.disableDnsResolver=true -Djava.net.preferIPv4Stack=true -Dvertx.logger-delegate-factory-class-name=io.vert"
        command = "kill $(ps aux | grep '" + subprocessIdentifier + "' | grep -v grep | awk '{print $2}')"
        subprocess.Popen(command, shell=True)

    def getTotalCash(self):
        accountNums = self.getAccountNums()

        ibkrCashTotal = 0

        for account in accountNums:
            ibkrCashTotal += self.getAccountCashValue(account)

        return ibkrCashTotal