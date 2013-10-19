from unittest import TestCase

import validator

class TestLoad_configuration(TestCase):
    def test_load_configuration(self):
        # when
        result = validator.load_configuration('test/test_config.json')

        # then
        self.assertEqual(result.get('size'), 2)
        self.assertEqual(len(result.get('columns')), 2)
