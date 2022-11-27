import unittest

from abs_value import absolute


class MyTestCase(unittest.TestCase):

    def test_absolute(self):
        self.assertEqual(5, absolute(-5))
        self.assertEqual(8, absolute(8))


if __name__ == '__main__':
    unittest.main()
