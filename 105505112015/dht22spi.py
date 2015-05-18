#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>


# dht22spi.py
#
# Read dht22 sensor using Raspberry Pi spi
#
# Daniel Perron
# 15 February 2014
# 

import spidev
import time



class dht22spi():

 

  def __init__(self, DeviceType="DHT22"):

    self.DHT22Type = (DeviceType == "DHT22")
    self.spi = spidev.SpiDev()
    self.speed = 500000
    self.spi.open(0,0)
    self.max_speed_hz=self.speed
    self.Bits = [ 128, 64, 32, 16, 8, 4, 2, 1]
    self.DHT22Reg = [0,0,0,0,0]

    #ok 10ms should be good enough
    MaxBits = 0.010 * self.speed
    self.ArraySize = int(MaxBits / 8)
    self.TotalBits = self.ArraySize * 8
    self.D = bytearray(self.ArraySize)

    # set first 1.5 ms Low and the rest high
    End = (0.0015 * self.speed)/8

    for i in range(self.ArraySize):
      if i > End:
        self.D[i] = 255
      else:
        self.D[i] = 0

  def GetBit(self,index):
    byteIndex = index / 8
    if (self.Data[byteIndex] &  self.Bits[index % 8]) == 0:
      return False
    return True

  def GetNextDelay(self):
    if self.LastIndex  >= self.TotalBits:
      return 0
    Index = self.LastIndex
    LastBit = self.GetBit(Index)
    while Index<self.TotalBits:
      if not (self.GetBit(Index) == LastBit):
        Delta = Index - self.LastIndex
        Deltaus = Delta * 1000000 / self.speed
        self.LastIndex = Index
        return Deltaus
      Index += 1


  ## this routine return  three values
  #   temperature , Humidity and  an boolean value to tell if the data is Valid

  def Read(self):
   self.LastIndex=0
   self.Data = list(self.D)
   self.spi.xfer2(self.Data)

   #first get rid off start
   self.GetNextDelay()

   #now get rid off wait
   self.GetNextDelay()

   #now get rid off Ack
   self.GetNextDelay()

   #and the the high Ack
   self.GetNextDelay()

   for Idx in range(5):
     self.DHT22Reg[Idx]=0
     for bitidx in range(8):
  
       #low parts
       self.GetNextDelay()

       #read High Parts
       delai = self.GetNextDelay()

       if delai < 12:
        return [None , None , False]

       if delai > 80:
        return [None , None , False]

       if delai > 43:
         self.DHT22Reg[Idx] |= self.Bits[bitidx]     

   #checksum
   Checksum = 0;
   for Idx in range(4):
     Checksum += self.DHT22Reg[Idx]
   Checksum %= 256

   #print "CheckSum= ", Checksum


   if Checksum == self.DHT22Reg[4]:
     if self.DHT22Type:
       Temp= ((self.DHT22Reg[2] & 127) * 256  + self.DHT22Reg[3]) / 10.0
       if (self.DHT22Reg[2] & 128) == 128:
         Temp = -Temp
       Humidity= (self.DHT22Reg[0] * 256 + self.DHT22Reg[1]) / 10.0
     else:
       Temp= self.DHT22Reg[2]
       Humidity = self.DHT22Reg[0]
   else:
     return [ None , None , False]

   return [Temp , Humidity , True]
   

if __name__ == '__main__':

  import time


  for  DHTType in ["DHT22", "DHT21"]:
  
    dht22 = dht22spi(DHTType)

    print "***************\nIf device is {0}\n".format(DHTType)

    value = dht22.Read()

    print "DHT returned values are " , dht22.DHT22Reg 


    if value[2]:
      print "Temperature = ", value[0], " Celsius"
      print "Humidity    = ", value[1], " %"
    else:
      print "Unable to read dht22 sensor"


    print "\n\n"
    time.sleep(1)
