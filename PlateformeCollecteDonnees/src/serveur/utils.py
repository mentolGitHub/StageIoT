
def print_SQL_response(cursor):
    for item in cursor:
        print(item)

def sql_var(str : str):
    """ check basique (injection possible mais ce n'est pas le sujet) \n
    on ne peut pas utiliser le %s pour certaines Query donc on fait un check minimal. """

    var = str.strip("--")
    var = var.strip(" ")

    return var