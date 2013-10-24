import logging
import re
import datetime

logging.basicConfig(level=logging.DEBUG)


class Validator:
    """Validator class validates provided data"""

    def __init__(self):
        self.logger = logging.getLogger('Validator')

    def validate_field(self, field):
        result = True
        result = self.__validate_field_required(field) and result
        result = self.__validate_field_max_length(field) and result
        result = self.__validate_field_min_length(field) and result
        result = self.__validate_field_possible_values(field) and result
        result = self.__validate_field_pattern(field) and result
        result = self.__validate_field_integer(field) and result
        result = self.__validate_field_date(field) and result

        return result

    def validate_record(self, record):
        result = self.__validate_record_size(record)
        for field in record.get_fields():
            result = self.validate_field(field) and result

        return result

    def validate_data(self, data):
        result = True
        for i, record in enumerate(data.get_records()):
            self.logger.info("****************** Record #%s validation ******************" % (i + 1))
            result = self.validate_record(record) and result

        return result

    def __log(self, result, message):
        if not result:
            self.logger.error(message)

    def __is_required(self, definition):
        return definition.get('required', False)

    def __validate_record_size(self, record):
        expected_size = record.get_expected_size()
        size = len(record.get_fields())
        result = size == expected_size
        self.__log(result, "Incorrect row size: %s (expected: %s)" % (size, expected_size))
        return result

    def __should_be_validated(self, definition, value, condition=True):
        return (self.__is_required(definition) or len(value.strip())) and condition

    def __validate_field_required(self, field):
        result = not self.__is_required(field.get_meta()) or field.get_value().strip()
        self.__log(result, "Missing %s field" % field.get_name())
        return bool(result)

    def __validate_field_max_length(self, field):
        max_length = field.get_meta().get('maxLength', 0)
        length = len(field.get_value())
        result = not max_length or length <= max_length
        self.__log(result, 'Too long %s field: %s (expected max length: %s)' % (field.get_name(), length, max_length))
        return result

    def __validate_field_min_length(self, field):
        meta_info = field.get_meta()
        value = field.get_value()
        result = True
        if self.__should_be_validated(meta_info, value):
            length = len(value.strip())
            min_length = meta_info.get('minLength', 0)
            result = length >= min_length
            self.__log(result,
                       'Too short %s field: %s (expected min length: %s)' % (field.get_name(), length, min_length))
        return result

    def __validate_field_possible_values(self, field):
        meta_info = field.get_meta()
        value = field.get_value()
        result = True
        possible_values = meta_info.get('values', [])
        if self.__should_be_validated(meta_info, value, possible_values):
            result = value in possible_values
            self.__log(result,
                       'Unexpected %s value: %s (acceptable values: %s)' % (field.get_name(), value, possible_values))
        return bool(result)

    def __validate_pattern(self, field, pattern):
        meta_info = field.get_meta()
        value = field.get_value()
        result = True
        if self.__should_be_validated(meta_info, value, pattern):
            result = re.match(pattern, value)
            self.__log(result, "%s value doesn't match pattern: %s (pattern: %s)" % (field.get_name(), value, pattern))
        return bool(result)

    def __validate_field_pattern(self, field):
        meta_info = field.get_meta()
        pattern = meta_info.get('pattern', '')

        if pattern and pattern[0] == pattern[-1] == '/':
            self.logger.warning('Unexpected regex delimiters: %s', pattern)
        if pattern and (pattern[0] != '^' or pattern[-1] != '$'):
            self.logger.warning('Missing ^$ delimiters for regex: %s', pattern)

        result = self.__validate_pattern(field, pattern)
        return bool(result)

    def __validate_field_integer(self, field):
        meta_info = field.get_meta()
        value = field.get_value()
        result = True
        is_integer = meta_info.get('integer', False)
        if is_integer:
            result = self.__validate_pattern(field, '^[0-9]+$')
            self.__log(result, "Incorrect %s integer value: %s" % (field.get_name(), value))
        return bool(result)

    def __validate_field_date(self, field):
        meta_info = field.get_meta()
        value = field.get_value()
        result = True
        date_format = meta_info.get('date', False)
        if self.__should_be_validated(meta_info, value, date_format):
            try:
                date_string = datetime.datetime.strptime(value, date_format).strftime(date_format)
                result = date_string == value
            except ValueError:
                result = False
            self.__log(result, "Incorrect %s date: %s (expected format: %s)" % (field.get_name(), value, date_format))
        return bool(result)
