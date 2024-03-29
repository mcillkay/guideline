import os
import re
from pathlib import Path

HEADER = '\033[95m'
PURPLE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


BREAKS = 'breaks'
TASK = 'task'
TYPE = 'type'
START = 'start'
STOP = 'stop'
AMOUNT = 'amount'
PLEDGE = 'pledge'
GROWTH_CURVE = 'growth_curve'
PERIOD = 'period'
SCHEDULE = 'schedule'
STRICT = 'strict'
LAX_TIME = 'lax_time'
STARTDATE = 'startdate'
TIMESHEET = 'timesheet'
MULTIPLE = 'multiple'

A = 10  #amplitude for sinusoidal growth curve

PROJECT_NAME = 'guideline'
DATA_DIR = 'data'
TEST_DIR = 'test'
CONTRACTS_FILE = 'contracts.csv'

FRACTION_REGEX = re.compile(r'^(\d+)(?:(?:\s+(\d+))?/(\d+))?$')

PROJECT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = PROJECT_PATH / DATA_DIR
TEST_PATH = PROJECT_PATH / TEST_DIR
# CONTRACTS_PATH = PROJECT_PATH / DATA_DIR / CONTRACTS_FILE

TIMESHEET_COLS = [START, STOP, AMOUNT, MULTIPLE]
CONTRACT_PROMPTS = ['name of task', 'number of hours per day']

USER_COLUMNS = ['name', 'created', 'pod']

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


