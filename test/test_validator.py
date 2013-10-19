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

    def test_validate_row_default_delimiter(self):
        # given
        validator = Validator({})
        validator.validate_extracted_row = MagicMock(return_value=True)

        # when
        validator.validate_row('test|test2')

        # then
        validator.validate_extracted_row.assert_called_once_with(['test', 'test2'])

    def test_validate_row_delimiter(self):
        # given
        validator = Validator({'delimiter': '#'})
        validator.validate_extracted_row = MagicMock(return_value=True)

        # when
        validator.validate_row('test|te#st2')

        # then
        validator.validate_extracted_row.assert_called_once_with(['test|te', 'st2'])