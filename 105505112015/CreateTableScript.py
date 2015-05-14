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



try:
    con = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )
    cur = con.cursor()  
    cur.execute("DROP TABLE IF EXISTS myTable")
    cur.execute("""CREATE TABLE myTable (
            mydate    DATE,
            mytimestamp TIMESTAMP,
            mytime  TIME,
            mystring varchar(30))""")
    query = """INSERT INTO myTable VALUES (
        %(mydate)s, %(mytimestamp)s, %(mytime)s, %(mystring)s)"""
    rows = ( \
            {'mydate': psycopg2.Date(2009, 12, 25),
             'mytimestamp': psycopg2.Timestamp(2009, 12, 15, 06, 30, 00),
             'mytime': psycopg2.Time(6, 30, 00),
             'mystring': 'message!'},
            {'mydate': psycopg2.DateFromTicks(time.time()),
             'mytime': psycopg2.TimeFromTicks(time.time()),
             'mytimestamp': psycopg2.TimestampFromTicks(time.time()),
             'mystring': None})
    cur.executemany(query, rows)
    con.commit()

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
