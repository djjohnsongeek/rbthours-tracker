from django.test import TestCase
from . import helper

# Create your tests here

# Test Models
# Test Views

# Test Custom Helper Functions
class ConvertMonthTestCase(TestCase):
    def test_month_is_correct(self):
        """ Integer is properly converted to Month String """
        self.assertEqual(helper.convert_month("1"), "January")
        self.assertEqual(helper.convert_month(1), "January")
        self.assertEqual(helper.convert_month("6"), "June")
        self.assertEqual(helper.convert_month("12"), "December")
        self.assertEqual(helper.convert_month(12), "December")
    
    def test_handles_non_numeric_args(self):
        """ Returns valueError if a non numerical input is supplied """
        with self.assertRaises(ValueError):
            helper.convert_month("hellos")
            helper.convert_month("23423.5")

    def test_handles_large_numbers(self):
        """ Returns ValueError if number is too big """
        with self.assertRaises(ValueError):
            helper.convert_month(23)
            helper.convert_month("13")

    def test_handles_negative_numbers(self):
        """ Properly handles negative number arguments """
        self.assertEqual(helper.convert_month(-5), "May")

    def test_handles_decimal_args(self):
        """ Properly rounds down on ALL float types"""
        self.assertEqual(helper.convert_month(2.3), "Febuary")
        self.assertEqual(helper.convert_month(2.9), "Febuary")

class StripRowIdsFromListOfDict(TestCase):
    def test_deletes_id_key_values(self):
        """ removes the id key value pairs from the given dictionary """

        EXAMPLE_LOD = [
            {"id": 1, "session_hours": 20, "obs_hours": 1},
            {"id": 2, "session_hours": 52, "obs_hours": 3}
        ]

        RESULT_LOD = [
            {"session_hours": 20, "obs_hours": 1},
            {"session_hours": 52, "obs_hours": 3}
        ]

        helper.strip_ids(EXAMPLE_LOD)
        self.assertEqual(RESULT_LOD, EXAMPLE_LOD)

    def test_handles_empty_list(self):
        """ returns empty list if given an empty list """
        self.assertEqual(helper.strip_ids([]), [])

    def test_handles_non_existent_key(self):
        """ raises KeyError if id key is not present """
        RESULT_LOD = [
            {"session_hours": 20, "obs_hours": 1},
            {"session_hours": 52, "obs_hours": 3}
        ]
        with self.assertRaises(KeyError):
            helper.strip_ids(RESULT_LOD)

    def test_returns_listOfInt(self):
        """ returns a list of integers """
        EXAMPLE_LOD = [
            {"id": 1, "session_hours": 20, "obs_hours": 1},
            {"id": 2, "session_hours": 52, "obs_hours": 3}
        ]
        self.assertEqual(helper.strip_ids(EXAMPLE_LOD), [1, 2])