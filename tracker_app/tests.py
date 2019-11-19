from django.test import TestCase, Client
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.messages import get_messages
from tracker_app.models import Daily_log, Monthly_log, User
from django.contrib.auth.models import Group
from . import helper

import os
import datetime
# ------------------------------ Test Models -------------------------------- #
class ModelsTestCase(TestCase):
    def setUp(self):
        """ Setup required Data Base Rows """
        helper.setup_test_db("all")

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

# ------------------------------- Test Views -------------------------------- #
class ViewsTestCase(TestCase):
    def setUp(self):
        helper.setup_test_db("all")

    def test_index_view(self):
        # user is not logged in
        c = Client()
        response = c.get("/")
        
        # redirects to login page
        self.assertEqual(response.status_code, 302)

        # user is logged in
        user = User.objects.get(pk=1)
        c.force_login(user, backend=None)
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

        # test request method other then get
        response = c.post("/", {"name": "Daniel"})
        self.assertEqual(response.status_code, 405) # method no allowed

    def test_login_view(self):
        user = User.objects.get(pk=1)
        today = datetime.date.today()
        one_year = datetime.timedelta(days=365)

        # update user password (this is done here instead of inside
        # helper.setup_test_db to increase test preformance)
        user.set_password("hashedpassword")
        user.save()
        c = Client()

        # --- GET request tests ---- #
        response = c.get("/login")

        # delete data file exists
        path = os.path.join(settings.BASE_DIR, "delete_date", "date.txt")
        self.assertTrue(os.path.exists(path))

        # get date
        with open(path, "r") as f:
            string_date = f.read()

        # convert date from file to date obj
        delete_date = datetime.datetime.strptime(string_date, "%m/%d/%Y").date()
        time_till_delete = delete_date - today

        # all logs are deleted if delete date is 'today'
        if delete_date == today + one_year:
            self.assertEqual(user.daily_logs.count(), 0)
            self.assertEqual(user.monthly_logs.count(), 0)
        # all logs intact otherwise
        else:
            self.assertEqual(user.daily_logs.count(), 2)
            self.assertEqual(user.monthly_logs.count(), 2)

        # login page is found
        self.assertEqual(response.status_code, 200)

        # ---- Post request tests ---- #
        # successful login attempt
        response = c.post("/login", {"username": "firstlast", "password": "hashedpassword"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertEqual(response.status_code, 302)

        # failed login attemp
        response = c.post("/login", {"username": "firstlast", "password": "fake"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Credentials")
        
        # ---- Other request tests ----
        response = c.delete("/login", {"password": "password", "username": "username"})
        self.assertEqual(response.status_code, 405)
    
    def test_supervisor_view(self):
        pass
        # TODO
            
# For each view:
    # - check for the correct response code
    # - check for correct content within the reponse context
    # - check data base entires are correctly modified (not not modified)
        # - daily log creates monthly log (if not monthly log)
        # - daily log does not create monthly log (if monthly log exists)


# ---------------------- Test Custom Helper Functions ----------------------- #
# TODO Test json_httpResponse()
# Test method_not_allowed()
class MethodNotAllowed(TestCase):
    def test_method_not_allowed(self):
        response = HttpResponse("Method Not Allowed")
        response.status_code = 405
        self.assertEqual(helper.method_not_allowed().status_code, response.status_code)
        self.assertEqual(helper.method_not_allowed().content, response.content)
        
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

# Test strip_ids()
class StripIdKeysFromListOfDict(TestCase):

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

# test is_member()
class IsMember(TestCase):
    def setUp(self):
        helper.setup_test_db("users")

    def test_is_member(self):
        """ user in group supervisor validates as such """
        supervisor = User.objects.get(pk=2)
        self.assertTrue(helper.is_member("Program Supervisor", supervisor))

    def test_is_not_member(self):
        """ regular user and superuser should not validate as a supervisor """
        user = User.objects.get(pk=1)
        superuser = User.objects.get(pk=3)
        self.assertFalse(helper.is_member("Program Supervisor", superuser))
        self.assertFalse(helper.is_member("Program Supervisor", user))
        self.assertFalse(helper.is_member("Editor", user))

    def test_invalid_args(self):
        """ raises value error if arguments are incorrect """
        user = User.objects.get(pk=1)
        with self.assertRaises(ValueError):
            helper.is_member("Program Supervisor", "User")
            helper.is_member(232, user)
