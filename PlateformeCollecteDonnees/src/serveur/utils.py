import mysql.connector.abstracts

def print_SQL_response(cursor : mysql.connector.abstracts.MySQLCursorAbstract):

    """
    Print the result of the cursor (as it is an iterable we lose it's content, useful for debug)
    """
    
    for item in cursor:
        print(item)

def sql_var(str : str):

    """
    Basic check  (injection is possible but it is not the subject) \n
    cant use the %s to replace var in some query so we still do a minimal sanitization.
    """

    var = str.strip("--")
    var = var.strip(" ")
    var = var.strip(";")

    return var