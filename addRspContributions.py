import logging

from googleSheetsWriter import GoogleSheetsWriter
from datetime import datetime
from logging.handlers import RotatingFileHandler

# The ID and range of a sample spreadsheet.
PORTFOLIO_SPREADSHEET_ID = '1M6ZNA_O1-T90ASBvttFo_hNroYqYCJKD_5SAjmBT1wg'
APPEND_RANGE = 'RSP Contributions!A2:C2'

# Set up logging
LOG_DIRECTORY = '/var/log/financeJobs'
LOG_FILE_PATH = f'{LOG_DIRECTORY}/rspUpdate.log'

#Path to directory where the .json files are stored
DIR_PATH = '/Users/andre/Workspace/portfolio-tracker-automation'

CONTRIBUTION_AMOUNT = 163.46

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE_PATH, maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)

def getDate():
    # Get the current date, then format
    current_date = datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y").replace(" 0", " ")

    return formatted_date

def main():
    try:
        writer = GoogleSheetsWriter()

        values = [getDate(), CONTRIBUTION_AMOUNT, CONTRIBUTION_AMOUNT]

        writer.appendValueToSheet(PORTFOLIO_SPREADSHEET_ID, APPEND_RANGE, values)
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    main()
