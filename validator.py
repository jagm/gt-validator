#!/usr/bin/python
#-*- coding: utf-8 -*-

import json


def load_configuration(config_file='config.json'):
    return json.load(open(config_file))


def load_data_file(data_file):
    return (line.rstrip('\n') for line in open(data_file, 'r'))


def main():
    configuration = load_configuration()


if __name__ == '__main__':
    main()