import unittest
import constants as c

class TestConstants(unittest.TestCase):

    def test_paths(self):
       	print(c.DATA_PATH)

if __name__ == '__main__':
    unittest.main()
    # t = TestSystem
    # t.test_axial_doppler
