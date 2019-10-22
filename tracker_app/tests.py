from django.test import TestCase
from django.db import IntegrityError
from tracker_app.models import Daily_log, Monthly_log, User
from django.contrib.auth.models import Group
from . import helper
"""-------------------------------------------------------------------------"""
# Test Models
class ModelsTestCase(TestCase):
    def setUp(self):
        """ Setup required Data Base Rows """
        # create user
        User.objects.create(
            id=1, 
            password="hashedpassword", 
            is_superuser="False",
            first_name="First", 
            last_name="Last", 
            username="firstlast"
        )
        user = User.objects.get(pk=1)

        # create Supervisor user
        User.objects.create(
            id=2, 
            password="hashedpassword2", 
            is_superuser="False",
            first_name="First2", 
            last_name="Last2", 
            username="firstlast2"
        )
        supervisor = User.objects.get(pk=2)

        # create Program Supervisor Group
        group_name = "Program Supervisor"
        new_group = Group(name=group_name)
        new_group.save()

        # add Supervisor user to Group
        supervisor.groups.add(new_group)

        # create daily logs
        Daily_log.objects.create(
            user_id=user, 
            date="2019-10-18", 
            session_hours=5.00, 
            observed_hours=0.23, 
            supervisor="Kate"
        )
        Daily_log.objects.create(
            user_id=user, 
            date="2019-11-18", 
            session_hours=2, 
            observed_hours=0, 
            supervisor="None"
        )

        # create monthly logs
        Monthly_log.objects.create(
            user_id=user, 
            month=1, 
            year=2019,
            session_hours=120.00, 
            observed_hours=7.54, 
            mutable=False
        )
        Monthly_log.objects.create(
            user_id=user, 
            month=2, 
            year=2019,
            session_hours=5, 
            observed_hours=.23, 
            mutable=True
        )

    def test_unique_daily_date(self):
        """ test for unqiue daily dates """
        user = User.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Daily_log.objects.create(
                user_id=user, 
                date="2019-10-18",
                session_hours=5.00, 
                observed_hours=0.23,
                supervisor="Kate"
            )

    def test_unique_monthly_date(self):
        """ test for unique monthly dates """
        user = User.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Monthly_log.objects.create(
                user_id=user,
                month=1, 
                year=2019,
                session_hours=200.00,
                observed_hours=10, 
                mutable=False
            )

    def test_logs_count(self):
        """ ensure user/logs relationship is working """
        user = User.objects.get(pk=1)
        self.assertEqual(user.daily_logs.count(), 2)
        self.assertEqual(user.monthly_logs.count(), 2)


    def test_is_supervisor(self):
        """ test if a user is in the supervisor group """
        supervisor = User.objects.get(pk=2)
        self.assertTrue(
            supervisor.groups.filter(name="Program Supervisor").exists()
        )

    def test_is_not_supervisor(self):
        """ test if a user is not in a supervisor group """
        user = User.objects.get(pk=1)
        self.assertFalse(
            user.groups.filter(name="Program Supervisor").exists()
        )

# ---- Test Views ---- #
# daily log creates monthly log (if not monthly log)
# daily log does not create monthly log (if monthly log exists)


# ---- Test Custom Helper Functions ---- #
# Test convert_month()
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

# Test strip_ids
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

# test is_member
def IsMemberOfGroup(TestCase):
    def setUp(self):
        # create user
        User.objects.create(
            id=1, 
            password="hashedpassword", 
            is_superuser="False",
            first_name="First", 
            last_name="Last", 
            username="firstlast"
        )
        user = User.objects.get(pk=1)

        # create Supervisor user
        User.objects.create(
            id=2, 
            password="hashedpassword2", 
            is_superuser="False",
            first_name="First2", 
            last_name="Last2", 
            username="firstlast2"
        )
        supervisor = User.objects.get(pk=2)

        # create Program Supervisor Group
        group_name = "Program Supervisor"
        new_group = Group(name=group_name)
        new_group.save()

        # add Supervisor user to Group
        supervisor.groups.add(new_group)

    def test_is_member(self):
        user = User.objects.get(pk=1)
        supervisor = User.objects.get(pk=2)

        self.assertTrue(helper.is_member("Program Supervisor", supervisor))
        self.assertFalse(helper.is_member("Program Supervisor", user))
        self.assertFalse(helper.is_member("Editor", user))
        with self.assertRaises(ValueError):
            helper.is_member("Program Supervisor", "User")
            helper.is_member(232, user)