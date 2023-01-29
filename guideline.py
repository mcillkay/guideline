#!/usr/bin/env python3
"""guideline

Usage:
guideline.py delete <task>
guideline.py display [<task>] [-d <date>]
guideline.py d [<task>] [-d <date>]
guideline.py derail [<task>] [-d <date>]
guideline.py edit <task>
guideline.py total <task>
guideline.py manual <task>
guideline.py new
guideline.py start <task>
guideline.py skip <task>
guideline.py plan
guideline.py schedule
guideline.py view <task>
guideline.py strict (enable|disable) <task>

Options:
-d <date>, --date <date>    Date in this format: 2021-01-21
-h, --help                  Show this screen
"""

#TODO: categorical tasks, time total for a task, different units (caffeine mg, cigarettes), strict mode, payments, pledge growth curves, pod algorithm, data analysis, skip task, sick + vacation, notes, personal best, live progress bar, different accounts (one for me and rowan eg), support for changing task name

#TODO: others using: if data dir not exist, make it,
#NOTE: keep data dir out of public github (that's private information)

import os
import data
import display
import pickle
import pandas as pd
import constants as c
from docopt import docopt
from pprint import pprint
from datetime import datetime, timedelta

if __name__ == '__main__':

    kwargs = docopt(__doc__, version='guideline 0.1')
    #print(kwargs)

    #Print current goals
    if kwargs['new']:
        n = datetime.now()
        days = int(input('Start in how many days? 0 for today, 1 for tomorrow, etc. > '))
        res = {c.STARTDATE: datetime(year=n.year, month=n.month, day=n.day + days)}

        res[c.TASK] = input('name of task > ')
        amount = input('hours per day > ' )
        res[c.AMOUNT] = float(amount) if '.' in amount else data.frac_to_float(input)
        res[c.SCHEDULE] = input('how many multiples of your per day do you want to work each day of the week? 0 for no work, 1 for base amount, 2 for twice that... only integers like this: 1121100 > \n\tMTWRFSS\n\t')
        assert len(res[c.SCHEDULE]) == 7
        res[c.PLEDGE] = float(input('$ committed per derail > '))
        res[c.STRICT] = int(input('1 for strict mode, 0 otherwise > '))
        assert res[c.STRICT] in [0, 1]
        res[c.LAX_TIME] = None
        res[c.TIMESHEET] = data.new_timesheet(res[c.TASK])

        task_path = c.DATA_PATH / res[c.TASK]

        if not os.path.exists(c.DATA_PATH):
            os.mkdir(c.DATA_PATH)

        if os.path.exists(c.DATA_PATH / task_path): #don't save over everything
            print(f'task {res[c.TASK]} already exists!')
        else:
            data.save_data(res)
            print(f'\ncreated task: {res[c.TASK]}')

    if kwargs['view']:
        res = data.load_data(kwargs['<task>'])
        pprint(res)

    #Start the timer
    if kwargs['start']:
        task = kwargs['<task>']
        res = data.load_data(task)
        df = res[c.TIMESHEET]

        start_time = datetime.now()
        df.loc[len(df), c.AMOUNT] = res[c.AMOUNT]
        df.loc[len(df)-1, c.START] = start_time
        data.save_data(res)

        print(f'\nstarted {c.OKCYAN}{task}{c.ENDC} at {display.format_date(start_time)}... work hard!')

        while True:

            user_input = input('\ntype \'stop\' to exit: > ')

            if user_input == "stop":

                stop_time = datetime.now()
                df.loc[len(df)-1, c.STOP] = stop_time

                data.save_data(res)

                delta = (stop_time - start_time).total_seconds()
                hours, minutes, seconds = data.parse_total_seconds(delta)
                print(f'worked for {hours} hours, {minutes} minutes, {seconds} seconds')

                break


    if kwargs['strict']:
        task = kwargs['<task>']
        res = data.load_data(task)

        if kwargs['enable']:
            flag = input('Are you sure? Enabling strict mode means you cannot change your task parameters until you disable strict mode, and disabling takes 7 days to come into effect. If you previously disabled strict mode, enabling it again before the 7 days have passed will reset the countdown to zero. Then you will have to wait 7 days to disable strict mode again. \n\nType YES if you are sure > ')
            if flag != 'YES':
                print('Strict mode NOT enabled. You are off the hook.')

            else:
                res[c.STRICT] = 1
                if res.get(c.LAX_TIME, False):
                    del res[c.LAX_TIME]
                data.save_data(res)
                print('Strict mode is enabled. Now you had better work hard!')

        elif kwargs['disable']:
            if not res[c.STRICT]:
                print('Strict mode not enabled in the first place.')
            else:
                res[c.LAX_TIME] = datetime.now() + timedelta(days=7)
                print(f'Strict mode will be disabled on {display.format_date(res[c.LAX_TIME])}. If you change your mind you can destroy this timer by enabling strict mode again.')
                data.save_data(res)


    if kwargs['total']:
        task = kwargs['<task>']
        res = data.load_data(task)
        h, m, s = data.parse_total_seconds(data.get_total_work_seconds(res))
        print(f'Total time of {h} hours, {m} minutes and {s} seconds on {task}')


    if kwargs['edit']:
        task = kwargs['<task>']
        res = data.load_data(task)
        if res[c.STRICT] and res[c.LAX_TIME] and datetime.now() < res[c.LAX_TIME]:
            print(f'Strict mode is enabled for {task}, unfortunately you cannot make any changes.')
        else:
            print('edit now, then continue (press \'c\') to save... BE CAREFUL!')
            breakpoint()
            data.save_data(res)
            print(f'saved changes to {c.DATA_PATH / res[c.TASK]}')


    #if you weren't at your computer while you were working
    if kwargs['manual']:
        length = float(input('how many minutes did you work? >'))
        start = input('when did you start? input like this: 2021-01-21 13:42 >')

        start_time = datetime.strptime(start, '%Y-%m-%d %H:%M')
        stop_time = start_time + timedelta(minutes=length)

        res = data.load_data(kwargs['<task>'])
        df = res[c.TIMESHEET]

        df.loc[len(df), c.AMOUNT] = res[c.AMOUNT]
        df.loc[len(df)-1, c.START] = start_time
        df.loc[len(df)-1, c.STOP] = stop_time

        data.save_data(res)

        print(f'saved entry in timesheet like this: \n{df.iloc[-1]}')

    #Print progress of goals
    if kwargs['display'] or kwargs['d']:
        if kwargs['<task>']:
            task = kwargs['<task>']
            display.get_progress_bar(task, datetime.now())
        else:
            tasks = c.DATA_PATH.glob('*')
            for task in tasks:
                display.get_progress_bar(task.name, datetime.now())

    #Print derails
    if kwargs['derail']:
        if kwargs['<task>']:
            task = kwargs['<task>']
            res = data.load_data(task)
            date = kwargs['date'] if kwargs.get('date', 0) else datetime.now()

            if date < res[c.STARTDATE]:
                print('task has not yet started...')

            else:
                goal_seconds = data.get_goal_seconds(res, date)
                days = (datetime.now() - res[c.STARTDATE]).days
                for d in range(1, days):
                    date = datetime.now() - timedelta(d)
                    work_seconds = data.get_work_seconds(res, date) #[c.TIMESHEET], date)
                    if work_seconds < goal_seconds:
                        print(f'{c.FAIL} DERAIL: {task} on {date}')

    #Print schedule
    if kwargs['schedule']:
        tasks = c.DATA_PATH.glob('*')
        display.schedule()
