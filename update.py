import constants as c
import data


def load_all_tasks():
    tasks = c.DATA_PATH.glob('*')
    for task in tasks:
        yield data.load_data(task.name)

#decorator to add type:more to res dict
def add_type(func):
    def inner(res):
        res[c.TYPE] = 'more'
        return func(res)
    return inner

#decorator to add pledge column to timesheet
def add_pledge(func):
    def inner(res):
        df = res[c.TIMESHEET]
        df[c.PLEDGE] = res[c.PLEDGE]
        return func(res)
    return inner

#decorator to add multiple column to timesheet
def add_multiple(func):
    def inner(res):
        df = res[c.TIMESHEET]
        df[c.MULTIPLE] = 0
        for idx in df.index:
            day = df.loc[idx, c.START].weekday()
            df.loc[idx, c.MULTIPLE] = int(res[c.SCHEDULE][day])
            res[c.TIMESHEET] = df
        return func(res)
    return inner

#decorator to add period to res dict
def add_period(func):
    def inner(res):
        res[c.PERIOD] = 1
        return func(res)
    return inner

#first update this and run to test you are not going to bork your data
@add_pledge
def update_test(res):
    breakpoint()

#decorate this properly and run script to update
@add_pledge
def update_res(res):
    data.save_data(res)


if __name__ == '__main__':
    for res in load_all_tasks():
        update_test(res)

