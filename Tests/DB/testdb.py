import mysql.connector


def print_SQL_response(cursor):
    for item in cursor:
        print(item)
    


mydb = mysql.connector.connect(host="localhost", user="root"
)

cursor = mydb.cursor()
db_name="mysql"

liste_db=[]
cursor.execute("show databases")
for i in cursor:
    liste_db+=i

print(liste_db)
if db_name in liste_db :
    query="use {};".format(db_name)
    print(query)
    cursor.execute(query)
    print_SQL_response(cursor)

else:
    exit(1)
liste_tables=[]
cursor.execute("show tables;")
for i in cursor:
    liste_tables+=i
print(liste_tables)

#for table in liste_tables:
table = liste_tables[2]
print(table)
try:
    cursor.execute("SELECT * FROM db")
    print_SQL_response(cursor)
finally:
    pass

print("coucou")