#!/usr/bin/python
#-*- coding: utf-8 -*-

import json


class Validator:
    """Validator class validates provided data"""

    def __init__(self, configuration):
        self.__configuration = configuration

    def validate_data(self, data):
        return True


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