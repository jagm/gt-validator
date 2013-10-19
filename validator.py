#!/usr/bin/python
#-*- coding: utf-8 -*-

import json


class Validator:
    """Validator class validates provided data"""

    def __init__(self, configuration):
        self.__configuration = configuration

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
        return len(row) == self.__get_expected_size()

    def __validate_field_required(self, definition, value):
        return not self.__is_required(definition) or value.strip()

    def __validate_field_max_length(self, definition, value):
        max_length = definition.get('maxLength', 0)
        return not max_length or len(value) <= max_length

    def __validate_field_min_length(self, definition, value):
        result = True
        length = len(value.strip())
        if self.__is_required(definition) or length:
            min_length = definition.get('minLength', 0)
            result = length >= min_length
        return result

    def __validate_field_possible_values(self, definition, value):
        result = True
        possible_values = definition.get('values', [])
        if value.strip() and possible_values:
            result = value in possible_values
        return result

    def validate_field(self, field, index):
        definition = self.__get_column_definition(index)
        result = True
        result = self.__validate_field_required(definition, field) and result
        result = self.__validate_field_max_length(definition, field) and result
        result = self.__validate_field_min_length(definition, field) and result
        result = self.__validate_field_possible_values(definition, field) and result
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
        for row in data:
            result = self.validate_row(row) and result

        return result


def load_configuration(config_file='data/config.json'):
    return json.load(open(config_file))


def load_data_file(data_file):
    return (line.rstrip('\n') for line in open(data_file, 'r'))


def main():
    configuration = load_configuration()
    data = load_data_file('data/flat_data.dat')
    validator = Validator(configuration)
    validator.validate_data(data)


if __name__ == '__main__':
    main()