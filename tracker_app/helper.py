from django.contrib.auth.models import User
"""-------------------------------------------------------------------------"""
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

