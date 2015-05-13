#!/usr/local/bin/python
import os
import sys
import psycopg2
import urlparse # import urllib.parse for python 3+
import RPi.GPIO as GPIO, time

result = urlparse.urlparse("postgres://mporyqeyslwjcx:dR3urCbiHhMi1cuFYn4qW7g6N3@ec2-184-73-165-195.compute-1.amazonaws.com:5432/d1thk2a4c7e2ma")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

con = None
GPIO.setmode(GPIO.BCM)
def RCtime (PiPin):
  measurement = 0
  GPIO.setup(PiPin, GPIO.OUT)
  GPIO.output(PiPin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(PiPin, GPIO.IN)
  while (GPIO.input(PiPin) == GPIO.LOW):
    measurement += 1
  return measurement



try:
    con = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )
    cur = con.cursor()

    
    
    for n in range(0,4):
      #print RCtime(4) # Measure timing using GPIO4
      print RCtime(4)

      cur.execute("INSERT INTO Cars VALUES(9,'x',2343)")
      cur.execute("SELECT * FROM Cars")
      con.commit()
      rows = cur.fetchall()
      for row in rows:
          print row

except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()   
