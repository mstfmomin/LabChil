#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import psycopg2
import urlparse # import urllib.parse for python 3+import psycopg2
import time


#Connecting to the Database
result = urlparse.urlparse("postgres://mporyqeyslwjcx:dR3urCbiHhMi1cuFYn4qW7g6N3@ec2-184-73-165-195.compute-1.amazonaws.com:5432/d1thk2a4c7e2ma")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

con = None
m =23


try:
    con = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )
    cur = con.cursor()  
    cur.execute("DROP TABLE IF EXISTS UID002A")
    cur.execute("""CREATE TABLE UID002A ( mytimestamp timestamp without time zone default (now() at time zone 'utc'), temperature double precision, humidity double precision)""")
    con.commit()

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
