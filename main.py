#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import json
import logging
from data.model import Data

from validator.validator import Validator

logging.basicConfig(level=logging.DEBUG)


def load_configuration(config_file='examples/config.json'):
    return json.load(open(config_file))


def load_data_file(data_file):
    return (line.rstrip('\n') for line in open(data_file, 'r'))


def main(data_file='examples/flat_data.dat', config_file='examples/config.json'):
    configuration = {}
    try:
        configuration = load_configuration(config_file)
    except IOError:
        logging.error("Cannot open file: %s" % config_file)
        exit()

    data = []
    try:
        data = load_data_file(data_file)
    except IOError:
        logging.error("Cannot open file: %s" % data_file)
        exit()

    data_object = Data(data, configuration)
    validator = Validator()
    validator.validate_data(data_object)


if __name__ == '__main__':
    length = len(sys.argv)
    if length == 2:
        main(sys.argv[1])
    elif length == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print "Incorrect arguments: %s. Provide file name to validate" % sys.argv
