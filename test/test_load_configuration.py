from unittest import TestCase
from main import load_configuration


class TestLoad_configuration(TestCase):
    def test_load_configuration(self):
        # when
        result = load_configuration('test/data/test_config.json')

        # then
        self.assertEqual(result.get('size'), 2)
        self.assertEqual(len(result.get('columns')), 2)
