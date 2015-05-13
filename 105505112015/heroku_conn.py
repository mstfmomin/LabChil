import os
import sys
import psycopg2
import urlparse # import urllib.parse for python 3+
result = urlparse.urlparse("postgres://mporyqeyslwjcx:dR3urCbiHhMi1cuFYn4qW7g6N3@ec2-184-73-165-195.compute-1.amazonaws.com:5432/d1thk2a4c7e2ma")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

con = None

cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
)

try:
    con = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )
    cur = con.cursor()

    cur = con.cursor()  
    
    cur.execute("DROP TABLE IF EXISTS Cars")
    cur.execute("CREATE TABLE Cars(Id INT PRIMARY KEY, Name TEXT, Price INT)")
    query = "INSERT INTO Cars (Id, Name, Price) VALUES (%s, %s, %s)"
    cur.executemany(query, cars)
        
    con.commit()

    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver

except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()   
