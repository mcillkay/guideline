import os
from pathlib import Path

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

TASK = 'task'
START = 'start'
STOP = 'stop'
AMOUNT = 'amount'
PLEDGE = 'pledge'
SCHEDULE = 'schedule'
STRICT = 'strict'
LAX_TIME = 'lax_time'
STARTDATE = 'startdate'
TIMESHEET = 'timesheet'

PROJECT_NAME = 'guideline'
DATA_DIR = 'data'
CONTRACTS_FILE = 'contracts.csv'

PROJECT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = PROJECT_PATH / DATA_DIR
# CONTRACTS_PATH = PROJECT_PATH / DATA_DIR / CONTRACTS_FILE

TIMESHEET_COLS = [START, STOP, AMOUNT]
CONTRACT_PROMPTS = ['name of task', 'number of hours per day']

USER_COLUMNS = ['name', 'created', 'pod']


