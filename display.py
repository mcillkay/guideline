import sys
import data
import constants as c
from datetime import datetime, timedelta

def get_color(percent, strict):
    color = c.ENDC
    if strict:
        color = c.WARNING
    if percent >= 100:
        color = c.OKGREEN
    if percent < 100:
        color = c.FAIL
    return color

def get_percent(work, goal):
    return round(100.0 * work / float(goal), 1)


def progress_bar(work, goal, date, suffix='', strict=False):
    bar_len = 60
    filled_len = min(bar_len, int(round(bar_len * work / float(goal))))

    percent = get_percent(work, goal)
    color = get_color(percent, strict)
    if color == c.FAIL and datetime.now().weekday() == date.weekday():
        color = c.ENDC

    bar = color + '\u2588' * filled_len + '\u2591' * (bar_len - filled_len)

    sys.stdout.write('%s %s%s \t%s\r' % (bar, percent, '%', suffix))
    sys.stdout.write('\n' + c.ENDC)#[%s] %s%s ...%s\r' % (bar, percent, '%', suffix))

    sys.stdout.flush()  # As suggested by Rom Ruben


def get_progress_bar(task, date):
    res = data.load_data(task)
    df = res[c.TIMESHEET]

    if datetime.now() < res[c.STARTDATE] or not data.goal_is_active(res, date):
        return

    if len(df) != 0 and type(df.loc[len(df)-1, c.STOP]) is not datetime: #currently working on task
        df.loc[len(df)-1, c.STOP] = datetime.now() #but don't save this

    goal_seconds = data.get_goal_seconds(res, date)
    work_seconds = data.get_work_seconds(res, date)

    progress_bar(
            work_seconds,
            goal_seconds,
            date,
            task + f' {res[c.AMOUNT]} hours',
            res[c.STRICT],
            )
# def print_row(task, status, color, max_task_len, max_day_len):
#     print(f' %{max_task_len}{task} %-10{s %-10s ' % (task, status, file_type)

def schedule():
    now = datetime.now()
    header = '%20s' % ('') + '\tMTWRFSS'#*8 % tuple([''] + c.WEEKDAYS)
    print(header)
    task_paths = c.DATA_PATH.glob('*')
    for path in task_paths:
        res = data.load_data(path)
        start_of_week = now - timedelta(days=now.weekday())
        line = []
        for d in range(7):
            date = start_of_week + timedelta(days=d)
            if date < res[c.STARTDATE]  or not data.goal_is_active(res, date):
                color = c.ENDC
                line.append(color+' ')
            else:
                goal_seconds = data.get_goal_seconds(res, date)
                work_seconds = data.get_work_seconds(res, date)
                percent = get_percent(work_seconds, goal_seconds)
                color = get_color(percent, res[c.STRICT])
                if color == c.FAIL and date >= now:
                    color = c.ENDC
                if color == c.ENDC and date.weekday() == now.weekday():
                    color = c.PURPLE
                line.append(color + 'X')

        to_print = '%20s' % res[c.TASK] + '\t' + ''.join(line)
        print(to_print)



def format_date(date):
    return date.strftime('%Y-%m-%d %H:%M')
