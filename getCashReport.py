from googleSheetsWriter import GoogleSheetsWriter
from wealthsimpleCash import wealthsimpleCash
from ibkrCash import IbkrCash

# The ID and range of a sample spreadsheet.
PORTFOLIO_SPREADSHEET_ID = '1M6ZNA_O1-T90ASBvttFo_hNroYqYCJKD_5SAjmBT1wg'
IBKR_CELL_NUM = 'Net Worth!B1'

def main():
    ibkr = IbkrCash()

    #Below steps will not work until the user is logged in
    input("Press Enter to continue once logged in...")

    ibkrCashTotal = ibkr.getTotalCash()
    ibkr.endPortalProcess()

    print(f"Total IBKR cash balance: {ibkrCashTotal}")

    ws = wealthsimpleCash()
    wsCashTotal = ws.getTotalCash()

    print(f"Total Wealthsimple cash balance: {wsCashTotal}")

    #numPsaShares = ws.getPsaShareCount()

    #print(f"Found {numPsaShares} shares of PSA.TO")

    writer = GoogleSheetsWriter()
    writer.writeValueToSheet(PORTFOLIO_SPREADSHEET_ID, IBKR_CELL_NUM, [[str(ibkrCashTotal)], [str(wsCashTotal)]])

if __name__ == '__main__':
    main()
