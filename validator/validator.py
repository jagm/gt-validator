import logging
import re
import datetime

logging.basicConfig(level=logging.DEBUG)


class Validator:
    """Validator class validates provided data"""

    def __init__(self, configuration):
        self.__configuration = configuration
        self.logger = logging.getLogger('Validator')

    def validate_field(self, field, index):
        definition = self.__get_column_definition(index)
        self.__set_default_field_name(definition, index)

        result = True
        result = self.__validate_field_required(definition, field) and result
        result = self.__validate_field_max_length(definition, field) and result
        result = self.__validate_field_min_length(definition, field) and result
        result = self.__validate_field_possible_values(definition, field) and result
        result = self.__validate_field_pattern(definition, field) and result
        result = self.__validate_field_integer(definition, field) and result
        result = self.__validate_field_date(definition, field) and result

        return result

    def validate_extracted_row(self, row):
        result = True
        result = self.__validate_row_size(row) and result
        for i, field in enumerate(row):
            result = self.validate_field(field, i) and result

        return result

    def validate_row(self, row):
        return self.validate_extracted_row(row.split(self.__get_delimiter()))

    def validate_data(self, data):
        result = True
        for i, record in enumerate(data.getRecords()):
            self.logger.info("****************** Record #%s validation ******************" % (i + 1))
            result = self.validate_row(record) and result

        return result

    def __log(self, result, message):
            if not result:
                self.logger.error(message)

    def __get_delimiter(self):
        return self.__configuration.get('delimiter', '|')

    def __get_expected_size(self):
        return self.__configuration.get('size', 0)

    def __get_column_definition(self, index):
        columns = self.__configuration.get('columns', [])
        return columns[index] if len(columns) > index else {}

    def __is_required(self, definition):
        return definition.get('required', False)

    def __validate_row_size(self, row):
        expected_size = self.__get_expected_size()
        size = len(row)
        result = size == expected_size
        self.__log(result, "Incorrect row size: %s (expected: %s)" % (size, expected_size))
        return result

    def __get_name_for_log(self, definition):
        return definition.get('name', '<unknown>')

    def __should_be_validated(self, definition, value, condition=True):
        return (self.__is_required(definition) or len(value.strip())) and condition

    def __validate_field_required(self, definition, value):
        result = not self.__is_required(definition) or value.strip()
        self.__log(result, "Missing %s field" % self.__get_name_for_log(definition))
        return bool(result)

    def __validate_field_max_length(self, definition, value):
        max_length = definition.get('maxLength', 0)
        length = len(value)
        result = not max_length or length <= max_length
        self.__log(result, 'Too long %s field: %s (expected max length: %s)' % (
        self.__get_name_for_log(definition), length, max_length))
        return result

    def __validate_field_min_length(self, definition, value):
        result = True
        if self.__should_be_validated(definition, value):
            length = len(value.strip())
            min_length = definition.get('minLength', 0)
            result = length >= min_length
            self.__log(result, 'Too short %s field: %s (expected min length: %s)' % (
            self.__get_name_for_log(definition), length, min_length))
        return result

    def __validate_field_possible_values(self, definition, value):
        result = True
        possible_values = definition.get('values', [])
        if self.__should_be_validated(definition, value, possible_values):
            result = value in possible_values
            self.__log(result, 'Unexpected %s value: %s (acceptable values: %s)' % (
            self.__get_name_for_log(definition), value, possible_values))
        return bool(result)

    def __validate_pattern(self, definition, pattern, value):
        result = True
        if self.__should_be_validated(definition, value, pattern):
            result = re.match(pattern, value)
            self.__log(result, "%s value doesn't match pattern: %s (pattern: %s)" % (
                self.__get_name_for_log(definition), value, pattern))
        return bool(result)

    def __validate_field_pattern(self, definition, value):
        result = True
        pattern = definition.get('pattern', '')

        if pattern and pattern[0] == pattern[-1] == '/':
            self.logger.warning('Unexpected regex delimiters: %s', pattern)
        if pattern and (pattern[0] != '^' or pattern[-1] != '$'):
            self.logger.warning('Missing ^$ delimiters for regex: %s', pattern)

        result = self.__validate_pattern(definition, pattern, value)
        return bool(result)

    def __validate_field_integer(self, definition, value):
        result = True
        is_integer = definition.get('integer', False)
        if is_integer:
            result = self.__validate_pattern(definition, '^[0-9]+$', value)
            self.__log(result, "Incorrect %s integer value: %s" % (self.__get_name_for_log(definition), value))
        return bool(result)

    def __validate_field_date(self, definition, value):
        result = True
        date_format = definition.get('date', False)
        if self.__should_be_validated(definition, value, date_format):
            try:
                date_string = datetime.datetime.strptime(value, date_format).strftime(date_format)
                result = date_string == value
            except ValueError:
                result = False
            self.__log(result, "Incorrect %s date: %s (expected format: %s)" % (self.__get_name_for_log(definition), value, date_format))
        return bool(result)

    def __set_default_field_name(self, definition, index):
        if not definition.get('name', False):
            definition['name'] = '<Field #%s>' % index
