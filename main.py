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


def main(data_file='examples/flat_data.dat'):
    configuration = {}
    try:
        configuration = load_configuration('examples/config.json')
    except IOError:
        logging.error("Cannot open file: %s" % 'examples/config.json')
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
    if len(sys.argv) != 2:
        logging.error("Incorrect arguments: %s. Provide file name to validate" % sys.argv)
    else:
        main(sys.argv[1])