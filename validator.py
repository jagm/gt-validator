#!/usr/bin/python
#-*- coding: utf-8 -*-

import json


class Validator:
    """Validator class validates provided data"""

    def __init__(self, configuration):
        self.__configuration = configuration

    def __get_delimiter(self):
        return self.__configuration.get('delimiter', '|')

    def validate_extracted_row(self, row):
        return True

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