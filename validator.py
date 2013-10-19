#!/usr/bin/python
#-*- coding: utf-8 -*-

import json


def load_configuration(config_file='config.json'):
    return json.load(open(config_file))
