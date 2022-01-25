import unittest

from app import helper


class HelperUnitTest(unittest.TestCase):
    def test_success(self):
        code = helper.generate_activation_code()

        assert len(code) == 4
