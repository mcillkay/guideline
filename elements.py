from datetime import datetime
import typing as tp





class Goal():
    ...
    #get royal society prize for tranqphil



class Day():
    '''
    '''
    def __init__(self):
        ...
        self.type = ... : ... #work, rest,


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
    '''
    def __init__(self):
        ...
        self.units = ... : 'Units'
        self.amount = ... :
        self.activity = ... : np.array #an array with 7 columns, and at least 1 row, of boolean values
        self.deadline = ...  : datetime
        self.repeat = ... : bool
        self.stake = ... : float
