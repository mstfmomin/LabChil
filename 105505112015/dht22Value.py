pi@raspberrypi ~/dht22spi $ cat dht22Value.py 
#!/usr/bin/python

import dht22spi
import time

dht22 = dht22spi.dht22spi()

value = dht22.Read()
time.sleep(0.5)
value = dht22.Read()
if value[2]:
  print "Temperature = ", value[0], " Celsius"
  print "Humidity    = ", value[1], " %"
else:
  print "Unable to read dht22 sensor"
