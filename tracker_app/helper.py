from django.contrib.auth.models import Group
from tracker_app.models import Daily_log, Monthly_log, User
from django.http import HttpResponse
import simplejson as json
"""-------------------------------------------------------------------------"""
def json_httpResponse(status: str, code: int, message:str):
    """
    String, Integer, String -> HttpResponse
    Returns a django httpResponse object that contains the given data (message
    and status) json encoded. HTTP response code is also set to provided "code".
    data and a status code
    """
    reponse = HttpResponse(json.dumps({
        "status": status,
        "message": message
    }))
    reponse.status_code = code
    return reponse

def method_not_allowed():
    """ 
    No Arugments -> httpResponse
    Returns a django httpResponse object with 304 status code
    """
    method_not_allowed = HttpResponse("Method Not Allowed")
    method_not_allowed.status_code = 405
    return method_not_allowed
    
def convert_month(num:str):
    """ 
    String or Integer or Float -> String
    Converts a numerical (string type) Month into its english equivlent
    For example: 1 converts to "Jan"
    """
    try:
        num = abs(int(num))
    except ValueError:
        raise ValueError
    if num > 12:
        raise ValueError
    
    months = [
        "January","Febuary","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    return(months[num - 1])

def strip_ids(list_of_dict:list):
    """ 
    ListOfDict -> List of Integers remove all of the id values from a list of
    dictionaries and return them in a list format
    """
    list_of_ids = []
    for row in list_of_dict:
        list_of_ids.append(row["id"])
        del row["id"]

    return list_of_ids

def is_member(group_name:str, user):
    """
    String User Obj-> Boolean
    Given a Django group name and a Django user object,
    produces true is the user is in the group otherwise returns false
    """
    try:
        return user.groups.filter(name=group_name).exists()
    except:
        raise ValueError

def setup_test_db(extent:str):
        """ 
        String -> Populates a test database with sample entries
        - Given string "all" populates database with user's and user logs
        - Given string "users" populates database with users
        - Otherwise raises ValueError
        NOTE: Do not use the function outside of an instance of Django's TestCase
        """

        # ensure proper args
        if extent not in {"users", "all"}:
            raise ValueError

        # create regular user
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
        
        # create Superuser
        User.objects.create(
            id=3, 
            password="hashedpassword3", 
            is_superuser=True,
            first_name="First3", 
            last_name="Last3", 
            username="firstlast3"
        )
        if extent == "all":
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