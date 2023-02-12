import unittest
import data
import constants as c
import pandas as pd
from datetime import datetime, timedelta

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        now = datetime(2023, 1, 23, 10) #monday
        yesterday = datetime(now.year, now.month, now.day-1) #sunday
        then = now + timedelta(hours=1) #monday
        yesterthen =  yesterday + timedelta(hours=1) #sunday
        later = then + timedelta(hours=2) #monday
        laterlater = later + timedelta(hours=2) #monday
        cls.df = pd.DataFrame({
            c.START: [yesterday, now, later],
            c.STOP:[yesterthen, then, laterlater]
            })
        cls.df[c.AMOUNT] = 1

        cls.now = now
        cls.res = {
                c.TIMESHEET : cls.df,
                c.SCHEDULE : '1121103',
                }

    def test_new_timesheet(self):
       	df = data.new_timesheet('Eratosthenes')
        # breakpoint()

    def test_get_timesheet_entries_on_date(self):
        a = data.get_timesheet_entries_on_date(self.df, self.now)
        self.assertTrue(len(a) == 2)

    def test_hours_to_seconds(self):
        self.assertTrue(data.hours_to_seconds(3) == 180*60)

    def test_get_work_seconds(self):
        work_seconds = data.get_work_seconds(self.res, self.now)
        self.assertTrue(work_seconds == 180*60)

    def test_get_goal_seconds(self):
        goal_seconds = data.get_goal_seconds(self.res, self.now)
        self.assertTrue(goal_seconds == 60*60)

        wednesday = self.now + timedelta(days=2)
        goal_seconds = data.get_goal_seconds(self.res, wednesday)
        self.assertTrue(goal_seconds == 60*60*2)

    def test_get_weekday(self):
        ...

if __name__ == '__main__':
    unittest.main()
    # t = TestConstants
    # t.test_axial_doppler
