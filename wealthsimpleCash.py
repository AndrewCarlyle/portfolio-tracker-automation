import wealthsimple

from cryptography.fernet import Fernet

PSA_CODE = 'sec-s-71db49aab4e446da936ec11ef05c2876'
EMAIL = "andrew.carlyle31@gmail.com"

class wealthsimpleCash:
    def __init__(self):
        self.ws = self.authenticate()
        self.accounts = self.ws.get_accounts()

    def myTwoFactorFunction(self):
        MFACode = ""
        while not MFACode:
            # Obtain user input and ensure it is not empty
            MFACode = input("Enter 2FA code: ")
        return MFACode

    def loadPass(self):
        with open('/Users/andre/.ssh/key.bin', 'rb') as file:
            key = file.read()

        with open('encryptedPass.bin', 'rb') as file:
            encryptedPass = file.read()

        return key, encryptedPass

    def authenticate(self):
        key, encryptedPass = self.loadPass()

        cipher_suite = Fernet(key)
        paswd = cipher_suite.decrypt(encryptedPass).decode()

        ws = wealthsimple.WSTrade(
            EMAIL,
            paswd,
            two_factor_callback=self.myTwoFactorFunction,
        )

        return ws

    def getTotalCash(self):
        cashTotal = 0

        for account in self.accounts:
            cashTotal += account['current_balance']['amount']

        return cashTotal
    
    def getPsaShareCount(self):
        for account in self.accounts:
            if PSA_CODE in account['position_quantities'].keys():
                return account['position_quantities'][PSA_CODE]