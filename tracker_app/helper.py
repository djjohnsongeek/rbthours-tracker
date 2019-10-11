
"""-------------------------------------------------------------------------"""
def convert_month(num:str):
    """ 
    Converts a numerical (string type) Month into its english equivlent
    For example: 1 converts to "Jan"
    """
    try:
        num = int(num)
    except ValueError:
        raise ValueError
    
    months = [
        "January","Febuary","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    return(months[num - 1])

def strip_ids(list_of_dict:list):
    """ 
    Dictionary -> List of Integers remove all of the id values from a list of
    dictionaries and return them in a list format
    """
    list_of_ids = []
    for row in list_of_dict:
        print(row)
        list_of_ids.append(row["id"])
        del row["id"]

    return list_of_ids

