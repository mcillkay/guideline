from datetime import datetime
import typing as tp


#TODO: how to add Personal Best! to tracking?
#NOTES: Should we pledge a max amount per cycle, or per plan? The cost of failure? or something?
#   in strict mode there is akrasia horizon


class Goal():
    ...
    #get royal society prize for tranqphil


class Day():
    '''
    '''
    def __init__(self):
        ...
        self.type: ... = ...#work, rest,


class Cycle():
    '''
    A Cycle is a sequence of Days
    '''
    ...


class Plan():
    '''
    A Plan is a sequence of Cycles
    '''
    ...
    #get royal society prize: finish book - write XXX chapters - read YYY - structure


class Units():
    ...
    #hours / minutes
    #milligrams


class Contract():
    '''
    TODO: think about how to do categorial 0-1 goals. a scalar goal w integer units an optional deadline and no repeats?
    '''

    def __init__(self):
        ...
        self.units: 'Units' = ...
        self.amount: = ...
        self.activity: np.array = ... #an array with 7 columns, and at least 1 row, of boolean values
        self.deadline: datetime = ...
        self.repeat: bool = ...
        self.stake: float = ...
        self.strict: bool = ...

        self.payment_schedule: Enum = ... # flat, linear and exponential
        self.last_payment: float = 0

        self.total_time = datetime.timedelta()

    def time_to_deadline(self) -> datetime.timedelta:
        now = datetime.datetime.now()
        remaining_time = self.deadline - now
        return remaining_time

    def start_timer(self):
        self.start_time = datetime.datetime.now()
        self.is_running = True

    def stop_timer(self):
        self.end_time = datetime.datetime.now()
        self.is_running = False
        elapsed_time = self.end_time - self.start_time
        self.total_time += elapsed_time

    def elapsed_time(self) -> datetime.timedelta:
        if self.is_running:
            now = datetime.datetime.now()
            elapsed_time = now - self.start_time
        else:
            elapsed_time = self.end_time - self.start_time
        return elapsed_time


