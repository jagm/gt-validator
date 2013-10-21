from unittest import TestCase
from main import load_data_file


class TestLoad_data_file(TestCase):
    def test_load_data_file(self):
        # given
        example = [
            'ABC|DEF',
            '123|456'
        ]

        # when
        data = load_data_file('test/data/test_flat_data.dat')

        #then
        for i, line in enumerate(data):
            self.assertEqual(line, example[i])
