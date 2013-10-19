from unittest import TestCase
from mock import MagicMock, call
from validator import Validator


class TestValidator(TestCase):
    def test_validate_data_empty(self):
        # given
        validator = Validator({})

        # when
        result = validator.validate_data([])

        # then
        self.assertTrue(result)

    def test_validate_data(self):
        # given
        validator = Validator({})

        # when
        result = validator.validate_data(['test', 'test2'])

        # then
        self.assertTrue(result)

    def test_validate_data(self):
        # given
        def return_value(data):
            if data == 'test':
                return True
            else:
                return False

        validator = Validator({})
        validator.validate_row = MagicMock(side_effect=return_value)

        # when
        result = validator.validate_data(['test', 'test2'])

        # then
        self.assertFalse(result)
        validator.validate_row.assert_has_calls([call('test'), call('test2')])
        self.assertEqual(validator.validate_row.call_count, 2)
