from unittest import TestCase
from mock import MagicMock, call
from validator import Validator


class TestValidator(TestCase):
    __default_validator = Validator({})

    def test_validate_data_empty(self):
        # given
        validator = self.__default_validator

        # when
        result = validator.validate_data([])

        # then
        self.assertTrue(result)

    def test_validate_data(self):
        # given
        validator = self.__default_validator

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

    def test_validate_extracted_row_correct_size(self):
        # given
        validator = Validator({'size': 2})

        # when
        result = validator.validate_extracted_row(['test', 'test2'])

        # then
        self.assertTrue(result)

    def test_validate_extracted_row_wrong_size(self):
        # given
        validator = Validator({'size': 3})

        # when
        result = validator.validate_extracted_row(['test', 'test2'])

        # then
        self.assertFalse(result)

    def test_validate_extracted_row(self):
        # given
        validator = Validator({'size': 2})
        validator.validate_field = MagicMock(return_value=True)

        # when
        result = validator.validate_extracted_row(['test', 'test2'])

        # then
        self.assertTrue(result)
        validator.validate_field.assert_has_calls([call('test', 0), call('test2', 1)])
        self.assertEqual(validator.validate_field.call_count, 2)

    def test_validate_extracted_row_required(self):
        # given
        validator = Validator({'size': 2, 'columns': [{'required': True}, {'required': False}]})

        # when
        result = validator.validate_extracted_row(['test', ''])

        # then
        self.assertTrue(result)

        # when
        result = validator.validate_extracted_row([' ', ' '])

        # then
        self.assertFalse(result)

    def test_validate_extracted_row_max_length(self):
        # given
        validator = Validator({'size': 3, 'columns': [{'maxLength': 4}, {'maxLength': 2}, {}]})

        # when
        result = validator.validate_extracted_row(['test', 'te', 'test1234'])

        # then
        self.assertTrue(result)

        # when
        result = validator.validate_extracted_row(['test', 'tes', 'test1234'])

        # then
        self.assertFalse(result)

        # when
        result = validator.validate_extracted_row(['test1', 'te', 'test1234'])

        # then
        self.assertFalse(result)

    def test_validate_extracted_row_min_length(self):
        # given
        validator = Validator({'size': 4, 'columns': [
            {'minLength': 2, 'required': True},
            {'minLength': 4, 'required': True},
            {'minLength': 6},
            {'required': True}
        ]})

        # when
        result = validator.validate_extracted_row(['test', 'test', '  ', 't'])

        # then
        self.assertTrue(result)

        # when
        result = validator.validate_extracted_row(['test', 'test', 'test', 'test'])

        # then
        self.assertFalse(result)

        # when
        result = validator.validate_extracted_row(['te', 'te', 'testtest', 'te'])

        # then
        self.assertFalse(result)
