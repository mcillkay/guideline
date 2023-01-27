import sys
import data
import constants as c
from datetime import datetime


def progress(count, total, suffix='', strict=False):
    bar_len = 60
    filled_len = min(bar_len, int(round(bar_len * count / float(total))))

    percents = round(100.0 * count / float(total), 1)

    color = c.ENDC
    if strict:
        color = c.WARNING
    if percents >= 100:
        color = c.OKGREEN

    bar = color + '\u2588' * filled_len + '\u2591' * (bar_len - filled_len)

    sys.stdout.write('%s %s%s \t%s\r' % (bar, percents, '%', suffix))
    sys.stdout.write('\n' + c.ENDC)#[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))

    # sys.stdout.flush()  # As suggested by Rom Ruben

def display(task, date):
    res = data.load_data(task)
    df = res[c.TIMESHEET]

    if datetime.now() < res[c.STARTDATE] or not data.goal_is_active(res, date):
        return

    if len(df) != 0 and type(df.loc[len(df)-1, c.STOP]) is not datetime: #currently working on task
        df.loc[len(df)-1, c.STOP] = datetime.now() #but don't save this

    goal_seconds = data.get_goal_seconds(res, date)
    work_seconds = data.get_work_seconds(res, date)

    progress(
            work_seconds,
            goal_seconds,
            task + f' {res[c.AMOUNT]} hours',
            res[c.STRICT]
            )

def format_date(date):
    return date.strftime('%Y-%m-%d %H:%M')
