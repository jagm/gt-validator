from unittest import TestCase
from mock import MagicMock, call
from data.model import Data, Record
from validator.validator import Validator


class TestValidator(TestCase):
    __default_validator = Validator()

    def test_validate_data_empty(self):
        # given
        validator = self.__default_validator

        # when
        result = validator.validate_data(Data([]))

        # then
        self.assertTrue(result)

        # when
        result = validator.validate_data(Data(['test', 'test2']))

        # then
        self.assertFalse(result)

    def test_validate_data(self):
        # given
        def return_value(data):
            if data.get_fields()[0].get_value() == 'test':
                return False
            else:
                return True

        validator = Validator()
        validator.validate_record = MagicMock(side_effect=return_value)
        data = Data(['test', 'test2'])
        expected_calls = [call(record) for record in data.get_records()]

        # when
        result = validator.validate_data(data)

        # then
        self.assertFalse(result)
        validator.validate_record.assert_has_calls(expected_calls)
        self.assertEqual(validator.validate_record.call_count, 2)

    def test_validate_row_size(self):
        # given
        configuration = {'size': 2}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'test|test2', 'result': True},
            {'values': 'test|test2|test3', 'result': False}
        ])

    def test_validate_row(self):
        # given
        record = Record('test|test2', {'size': 2})
        expected_calls = [call(field, record) for field in record.get_fields()]
        validator = Validator()
        validator.validate_field = MagicMock(return_value=True)

        # when
        result = validator.validate_record(record)

        # then
        self.assertTrue(result)
        validator.validate_field.assert_has_calls(expected_calls)
        self.assertEqual(validator.validate_field.call_count, 2)

    def test_validate_row_required(self):
        # given
        configuration = {'size': 2, 'columns': [{'required': True}, {'required': False}]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'test|', 'result': True},
            {'values': ' |', 'result': False}
        ])

    def test_validate_row_max_length(self):
        # given
        configuration = {'size': 3, 'columns': [{'maxLength': 4}, {'maxLength': 2}, {}]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'test|te|test1234', 'result': True},
            {'values': 'test|tes|test1234', 'result': False},
            {'values': 'test1|te|test1234', 'result': False}
        ])

    def test_validate_row_min_length(self):
        # given
        configuration = {'size': 4, 'columns': [
            {'minLength': 2, 'required': True},
            {'minLength': 4, 'required': True},
            {'minLength': 6},
            {'required': True}
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'test|test|  |t', 'result': True},
            {'values': 'test|test|test|test', 'result': False},
            {'values': 'te|te|testtest|te', 'result': False}
        ])

    def test_validate_row_possible_values(self):
        # given
        configuration = {'size': 4, 'columns': [
            {'values': ['test', 'test2'], 'required': True},
            {'values': ['test', 'test2', 'test3'], 'required': True},
            {'values': ['test', 'test2']},
            {'values': ['test', 'test2']}
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'test2|test3| |test2', 'result': True},
            {'values': 'test3|test3| |test2', 'result': False},
            {'values': 'test2|test4| |test2', 'result': False},
            {'values': 'test2|test3|test3|test2', 'result': False}
        ])

    def test_validate_row_pattern(self):
        # given
        configuration = {'size': 4, 'columns': [
            {'pattern': '^[A-Z]+$', 'required': True},
            {'pattern': '^[0-9]+$', 'required': True},
            {'pattern': '^[a-z]+$'},
            {'pattern': '^[A-Za-z0-9]+$'},
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': 'ABC|1234| |Test12', 'result': True},
            {'values': 'ABc|1234| |Test12', 'result': False},
            {'values': 'ABC|1234a| |Test12', 'result': False},
            {'values': 'ABC|1234| |Test#12', 'result': False},
        ])

    def test_validate_row_integer(self):
        # given
        configuration = {'size': 3, 'columns': [
            {'integer': True, 'required': True},
            {'integer': False, 'required': True},
            {'integer': True}
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': '1234|ABC| ', 'result': True},
            {'values': '1234|ABC|123', 'result': True},
            {'values': '123H|ABC| ', 'result': False},
            {'values': '1234|ABC|ABC', 'result': False}
        ])

    def test_validate_row_date(self):
        # given
        configuration = {'size': 3, 'columns': [
            {'date': '%Y%m%d', 'required': True},
            {'required': True},
            {'date': '%Y%m%d'}
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': '20131012|ABC| ', 'result': True},
            {'values': '20131012|ABC|ABC', 'result': False},
            {'values': '20131012|ABC|2013101', 'result': False},
            {'values': '20131312|ABC|  ', 'result': False},
            {'values': '20131032|ABC|  ', 'result': False},
        ])

    def test_validate_row_required_if_empty(self):
        # given
        configuration = {'size': 2, 'columns': [
            {},
            {'requiredIfEmpty': 0},
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': '1|2', 'result': True},
            {'values': '1|  ', 'result': True},
            {'values': ' |2', 'result': True},
            {'values': '|  ', 'result': False}
        ])

    def test_validate_row_required_if_empty_exception(self):
        # given
        configuration = {'size': 2, 'columns': [
            {'requiredIfEmpty': 2},
            {}
        ]}
        validator = Validator()

        # when, then
        try:
            self.__repeat(validator, configuration, [
                {'values': '1|2', 'result': False},
            ])
            self.fail("IndexError exception expected")
        except IndexError:
            pass # as expected

    def test_validate_row_required_if_filled(self):
        # given
        configuration = {'size': 2, 'columns': [
            {},
            {'requiredIfFilled': 0},
        ]}
        validator = Validator()

        # when, then
        self.__repeat(validator, configuration, [
            {'values': '1|2', 'result': True},
            {'values': '1|  ', 'result': False},
            {'values': ' |2', 'result': True},
            {'values': '|  ', 'result': True}
        ])

    def __repeat(self, validator, configuration, test_cases):
        for test_case in test_cases:
            # when
            result = validator.validate_record(Record(test_case['values'], configuration))

            # then
            self.assertTrue(result == test_case['result'])
