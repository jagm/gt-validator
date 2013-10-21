from unittest import TestCase
from data.model import Record


class TestRecord(TestCase):
    def test_validate_row_default_delimiter(self):
        # when
        fields = Record('test|test2', {}).get_fields()

        # then
        self.assertEqual(len(fields), 2)
        self.assertEqual([field.get_value() for field in fields], ['test', 'test2'])

    def test_validate_row_delimiter(self):
        # when
        fields = Record('test|te#st2', {'delimiter': '#'}).get_fields()

        # then
        self.assertEqual(len(fields), 2)
        self.assertEqual([field.get_value() for field in fields], ['test|te', 'st2'])
