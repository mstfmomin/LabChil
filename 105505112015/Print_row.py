#!/usr/local/bin/python
import os
import sys
import psycopg2
import urlparse # import urllib.parse for python 3+
import RPi.GPIO as GPIO, time



#Connecting to the Database
result = urlparse.urlparse("postgres://mporyqeyslwjcx:dR3urCbiHhMi1cuFYn4qW7g6N3@ec2-184-73-165-195.compute-1.amazonaws.com:5432/d1thk2a4c7e2ma")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

con = None

#Getting input from the GPIO
GPIO.setmode(GPIO.BCM)
def RCtime (PiPin):
  measurement = 0
  GPIO.setup(PiPin, GPIO.OUT)
  GPIO.output(PiPin, GPIO.LOW)
  time.sleep(1)

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
    print "Connected to Heroku"
    cur = con.cursor()
    while True:
      temp = RCtime(4)
      #time.sleep(5)
      cur.execute("INSERT INTO UID001A (Temparature) VALUES ('"+str(RCtime(4))+"')")
      cur.execute("SELECT * FROM UID001A ORDER BY mytimestamp DESC LIMIT 1")
      con.commit()
      #time.sleep(5)                    
      rows = cur.fetchall()
      for row in rows:
          print row
        # Drop the table if needed
        #cur.execute("DROP TABLE IF EXISTS Cars")
        #con.commit()         
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
#time.sleep(5)        
