import unittest
import display

class TestConstants(unittest.TestCase):

    def test_bar(self):
       	display.progress(10, 30, 'wow')

if __name__ == '__main__':
    unittest.main()
    # t = TestSystem
    # t.test_axial_doppler
