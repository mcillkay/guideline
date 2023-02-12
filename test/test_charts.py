import unittest
import test_data
import constants as c
import pandas as pd
from charts import charts
from datetime import datetime, timedelta

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res = data.load_test_data('GUIDELINE')

    def test_task_chart(self):
        breakpoint()

        ...

if __name__ == '__main__':
    unittest.main()
    # t = TestConstants
    # t.test_axial_doppler
