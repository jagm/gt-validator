from unittest import TestCase
from mock import MagicMock, call
from validator.validator import Validator


class TestValidator(TestCase):
    __default_validator = Validator({})

    def test_validate_data_empty(self):
        # given
        validator = self.__default_validator

        # when
        result = validator.validate_data([])

        # then
        self.assertTrue(result)

        # when
        result = validator.validate_data(['test', 'test2'])

        # then
        self.assertFalse(result)

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

    def test_validate_extracted_row_size(self):
        # given
        validator = Validator({'size': 2})

        self.__repeat(validator, [
            {'values': ['test', 'test2'], 'result': True},
            {'values': ['test', 'test2', 'test3'], 'result': False}
        ])

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

        self.__repeat(validator, [
            {'values': ['test', ''], 'result': True},
            {'values': [' ', ''], 'result': False}
        ])

    def test_validate_extracted_row_max_length(self):
        # given
        validator = Validator({'size': 3, 'columns': [{'maxLength': 4}, {'maxLength': 2}, {}]})

        self.__repeat(validator, [
            {'values': ['test', 'te', 'test1234'], 'result': True},
            {'values': ['test', 'tes', 'test1234'], 'result': False},
            {'values': ['test1', 'te', 'test1234'], 'result': False}
        ])

    def test_validate_extracted_row_min_length(self):
        # given
        validator = Validator({'size': 4, 'columns': [
            {'minLength': 2, 'required': True},
            {'minLength': 4, 'required': True},
            {'minLength': 6},
            {'required': True}
        ]})

        self.__repeat(validator, [
            {'values': ['test', 'test', '  ', 't'], 'result': True},
            {'values': ['test', 'test', 'test', 'test'], 'result': False},
            {'values': ['te', 'te', 'testtest', 'te'], 'result': False}
        ])

    def test_validate_extracted_row_possible_values(self):
        # given
        validator = Validator({'size': 4, 'columns': [
            {'values': ['test', 'test2'], 'required': True},
            {'values': ['test', 'test2', 'test3'], 'required': True},
            {'values': ['test', 'test2']},
            {'values': ['test', 'test2']}
        ]})

        self.__repeat(validator, [
            {'values': ['test2', 'test3', ' ', 'test2'], 'result': True},
            {'values': ['test3', 'test3', ' ', 'test2'], 'result': False},
            {'values': ['test2', 'test4', ' ', 'test2'], 'result': False},
            {'values': ['test2', 'test3', 'test3', 'test2'], 'result': False}
        ])

    def test_validate_extracted_row_pattern(self):
        # given
        validator = Validator({'size': 4, 'columns': [
            {'pattern': '^[A-Z]+$', 'required': True},
            {'pattern': '^[0-9]+$', 'required': True},
            {'pattern': '^[a-z]+$'},
            {'pattern': '^[A-Za-z0-9]+$'},
        ]})

        self.__repeat(validator, [
            {'values': ['ABC', '1234', ' ', 'Test12'], 'result': True},
            {'values': ['ABc', '1234', ' ', 'Test12'], 'result': False},
            {'values': ['ABC', '1234a', ' ', 'Test12'], 'result': False},
            {'values': ['ABC', '1234', ' ', 'Test#12'], 'result': False},
        ])

    def test_validate_extracted_row_integer(self):
        # given
        validator = Validator({'size': 3, 'columns': [
            {'integer': True, 'required': True},
            {'integer': False, 'required': True},
            {'integer': True}
        ]})

        self.__repeat(validator, [
            {'values': ['1234', 'ABC', ' '], 'result': True},
            {'values': ['1234', 'ABC', '123'], 'result': True},
            {'values': ['123H', 'ABC', ' '], 'result': False},
            {'values': ['1234', 'ABC', 'ABC'], 'result': False}
        ])

    def test_validate_extracted_row_date(self):
        # given
        validator = Validator({'size': 3, 'columns': [
            {'date': '%Y%m%d', 'required': True},
            {'required': True},
            {'date': '%Y%m%d'}
        ]})

        self.__repeat(validator, [
            {'values': ['20131012', 'ABC', ' '], 'result': True},
            {'values': ['20131012', 'ABC', 'ABC'], 'result': False},
            {'values': ['20131012', 'ABC', '2013101'], 'result': False},
            {'values': ['20131312', 'ABC', '  '], 'result': False},
            {'values': ['20131032', 'ABC', '  '], 'result': False},
        ])

    def __repeat(self, validator, test_cases):
        for test_case in test_cases:
            # when
            result = validator.validate_extracted_row(test_case['values'])

            # then
            self.assertTrue(result == test_case['result'])
