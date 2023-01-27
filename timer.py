from datetime import datetime

class Timer():
    '''
    '''
    def __init__(self):
        self.is_running = False

    def start_timer(self):
        self.start_time = datetime.datetime.now()
        self.is_running = True
        return self.start_time

    def stop_timer(self):
        self.end_time = datetime.datetime.now()
        self.is_running = False
        return self.end_time

    def elapsed_time(self):
        return datetime.datetime.now() - self.start_time
