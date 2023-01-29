import re
import pandas as pd
from datetime import datetime
import constants as c
import pickle

class Data():
    '''
    '''
    def __init__(self):
        ...

    def new_user(self, user):
        self.df = pd.DataFrame(c.DATA_COLUMNS)
        self.save_data(user)
        return df

    def new_goal(self, user, goal):
        self.df = pd.read_csv(c.DATA_PATH + user)
        return df

    def load_data(self, user):
        self.df = pd.read_csv(c.DATA_PATH + user)
        return df

    def save_data(self, user):
        self.df.to_csv(c.DATA_PATH + user)

def hours_to_seconds(hours):
    return hours * 60**2

def new_timesheet(task):
    df = pd.DataFrame(columns=c.TIMESHEET_COLS)
    df.index.name = task
    return df

def load_data(task):
    with open(c.DATA_PATH / task, 'rb') as to_load:
        return pickle.load(to_load)

def save_data(res):
    with open(c.DATA_PATH / res[c.TASK], 'wb') as to_save:
        pickle.dump(res, to_save)

def get_timesheet_entries_before_date(df, date):
    return df[df[c.START] < date]

def get_timesheet_entries_on_date(df, date):
    y, m, d = date.year, date.month, date.day
    midnight = datetime(y, m, d)
    midnight_tomorrow = datetime(y, m, d + 1)
    return df[(df[c.START] >= midnight) & (df[c.START] < midnight_tomorrow)]

def update_timesheet(res, start_time, stop_time):
    df = res[c.TIMESHEET]
    df.loc[len(df), c.AMOUNT] = res[c.AMOUNT]
    df.loc[len(df)-1, c.START] = start_time

    df = res[c.TIMESHEET]
    df.loc[len(df)-1, c.STOP] = stop_time
    return df

def parse_total_seconds(n):
    hours = n // 3600
    minutes = (n % 3600) // 60
    seconds = round(n % 60, 1)
    return hours, minutes, seconds

def get_goal_seconds(res, date):
    df = get_timesheet_entries_on_date(res[c.TIMESHEET], date)

    if len(df) != 0: #no entries that date
        hours = df.iloc[-1][c.AMOUNT]
    else:
        df = get_timesheet_entries_before_date(res[c.TIMESHEET], date)

        if len(df) != 0: #no entries that date
            hours = df.iloc[-1][c.AMOUNT]
        else:
            hours = res[c.AMOUNT]

    multiple =  get_work_multiple(res, date)
    return hours_to_seconds(hours) * multiple

def get_total_work_seconds(res):
    df = res[c.TIMESHEET]

    deltas = df[c.STOP] - df[c.START]
    if len(deltas) == 0:
        return 0

    return deltas.sum().total_seconds()

def get_work_seconds(res, date):
    df = get_timesheet_entries_on_date(res[c.TIMESHEET], date)

    deltas = df[c.STOP] - df[c.START]
    if len(deltas) == 0:
        return 0

    return deltas.sum().total_seconds()

def get_work_multiple(res, date):
    return int(res[c.SCHEDULE][date.weekday()])

def goal_is_active(res, date):
    return get_work_multiple(res, date)

# matches a string consisting of an integer followed by either a divisor
# ("/" and an integer) or some spaces and a simple fraction (two integers
# separated by "/")
FRACTION_REGEX = re.compile(r'^(\d+)(?:(?:\s+(\d+))?/(\d+))?$')

def frac_to_float(x):
  i, n, d = FRACTION_REGEX.match(x).groups()
  if d is None: n, d = 0, 1  # if d is None, then n is also None
  if n is None: i, n = 0, i
  return float(i) + float(n) / float(d)
