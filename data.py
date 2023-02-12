import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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

def load_test_data(task):
    with open(c.TEST_PATH / c.DATA_DIR / task, 'rb') as to_load:
        return pickle.load(to_load)

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
    midnight_tomorrow = datetime(y, m, d) + timedelta(days=1)
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

        if len(df) != 0:
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

def get_weekday(res, date):
    delta = date - res[c.STARTDATE]
    days = delta.days + res[c.STARTDATE].weekday()
    return days % (7 * res[c.PERIOD])


def get_work_multiple(res, date):
    return int(res[c.SCHEDULE][get_weekday(res, date)])
    # df = get_timesheet_entries_on_date(res[c.TIMESHEET], date)
    # if len(df) != 0:
    #     return df.iloc[-1][c.MULTIPLE]
    # else:
    #     df = get_timesheet_entries_before_date(res[c.TIMESHEET], date)

    #     if len(df) != 0:
    #         return df.iloc[-1][c.MULTIPLE]
    #     else:
    #         return int(res[c.SCHEDULE][date.weekday()])

def goal_is_active(res, date):
    return get_work_multiple(res, date)

# matches a string consisting of an integer followed by either a divisor
# ("/" and an integer) or some spaces and a simple fraction (two integers
# separated by "/")

def frac_to_float(x):
  i, n, d = c.FRACTION_REGEX.match(x).groups()
  if d is None: n, d = 0, 1  # if d is None, then n is also None
  if n is None: i, n = 0, i
  return float(i) + float(n) / float(d)


def skip(task, date, reason):
    res = load_data(task)
    if res[c.STRICT]:
        print(f'You cannot skip {task}, it is in strict mode!')
        return
    res[c.BREAKS].append((date, reason))
    save_data(res)

def growth_curve(base, num, curve):
    #given base pledge rate and number of iterations, return current pledge amount
    if curve == 0:
        return base

    elif curve == 1: #linear
        return base * num

    elif curve == 2: #exponential
        return base * np.exp(num/2)

    else: #sinusoidal
        return  base + (1 + c.A*np.cos((num+6)*np.pi/6))

