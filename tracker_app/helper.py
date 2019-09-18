
"""-------------------------------------------------------------------------"""
def convert_month(num:str):
    """ 
    Converts a numerical (string type) Month into its english equivlent
    For example: 1 converts to "Jan"
    """
    try:
        num = int(num)
    except ValueError:
        return(False)
    
    months = [
        "January","Febuary","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    return(months[num - 1])