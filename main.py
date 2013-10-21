#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import json
import logging

from validator.validator import Validator

logging.basicConfig(level=logging.DEBUG)


def load_configuration(config_file='data/config.json'):
    return json.load(open(config_file))


def load_data_file(data_file):
    return (line.rstrip('\n') for line in open(data_file, 'r'))


def main(data_file='data/flat_data.dat'):
    configuration = {}
    try:
        configuration = load_configuration('data/config.json')
    except IOError:
        logging.error("Cannot open file: %s" % 'data/config.json')
        exit()

    data = []
    try:
        data = load_data_file(data_file)
    except IOError:
        logging.error("Cannot open file: %s" % data_file)
        exit()

    validator = Validator(configuration)
    validator.validate_data(data)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("Incorrect arguments: %s. Provide file name to validate" % sys.argv)
    else:
        main(sys.argv[1])