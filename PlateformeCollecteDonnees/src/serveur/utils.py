import mysql.connector


def print_SQL_response(cursor):
    for item in cursor:
        print(item)
    