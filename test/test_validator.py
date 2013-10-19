from unittest import TestCase
from validator import Validator


class TestValidator(TestCase):
    def test_validate_data_empty(self):
        # given
        validator = Validator({})

        # when
        result = validator.validate_data([])

        # then
        self.assertTrue(result)


