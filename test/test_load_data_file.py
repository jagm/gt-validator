from unittest import TestCase
import validator


class TestLoad_data_file(TestCase):
    def test_load_data_file(self):
        # given
        example = [
            'ABC|DEF',
            '123|456'
        ]

        # when
        data = validator.load_data_file('test/data/test_flat_data.dat')

        #then
        for i, line in enumerate(data):
            self.assertEqual(line, example[i])
