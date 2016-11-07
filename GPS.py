#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : GPS.py
# Author  : Nicolas ISAERT
# Date    : 17/10/2016
# Version : 1.0 - Created
#
#------------------------------------------------

import serial
import os

DEBUG = True  #if DEBUG == True:print("")

class GPS:
#------------------------------------------------
   def __init__(self):
      # Set up serial:
      self.SerialGPS = serial.Serial(
         port='/dev/ttyUSB0',\
         baudrate=4800,\
         parity=serial.PARITY_NONE,\
         stopbits=serial.STOPBITS_ONE,\
         bytesize=serial.EIGHTBITS,\
         timeout=1)

      self.FirstFixFlag = False # this will go true after the first GPS fix.
      self.FirstFixDate = ""

      self.GPRMC = {
                  'fix_time': '000000.000',
                  'validity': 'A',
                  'latitude': '0000.0000',
                  'latitude_hemisphere' : 'N',
                  'longitude' : '00000.0000',
                  'longitude_hemisphere' : 'E',
                  'SOG': '0.00',
                  'COG': '000.00',
                  'fix_date': '000000',
                  'variation': '',
                  'variation_e_w' : '',
                  'checksum' : ''
      }

#------------------------------------------------
# Helper function to take HHMM.SS, Hemisphere and make it decimal
   def degrees_to_decimal(self, data, hemisphere):
      try:
         decimalPointPosition = data.index('.')
         degrees = float(data[:decimalPointPosition-2])
         minutes = float(data[decimalPointPosition-2:])/60
         output = degrees + minutes
         if hemisphere is 'N' or hemisphere is 'E':
            return output
         if hemisphere is 'S' or hemisphere is 'W':
            return -output
      except:
         return ""

#------------------------------------------------
# Helper function to take a $GPRMC sentence, and turn it into a Python dictionary.
   def parse_GPRMC(self, data):
      data = data.split(',')
      self.GPRMC = {
               'fix_time': data[1],
               'validity': data[2],
               'latitude': data[3],
               'latitude_hemisphere' : data[4],
               'longitude' : data[5],
               'longitude_hemisphere' : data[6],
               'SOG': data[7],
               'COG': data[8],
               'fix_date': data[9],
               'variation': data[10],
               'variation_e_w' : data[11],
               'checksum' : data[12]
      }
      self.GPRMC['decimal_latitude'] = self.degrees_to_decimal(self.GPRMC['latitude'], self.GPRMC['latitude_hemisphere'])
      self.GPRMC['decimal_longitude'] = self.degrees_to_decimal(self.GPRMC['longitude'], self.GPRMC['longitude_hemisphere'])
      return self.GPRMC

#------------------------------------------------
   def Communicate(self):
      NMEAdata = self.SerialGPS.readline()
      #print NMEAdata
      if "$GPRMC" in NMEAdata: # This will exclude other NMEA sentences the GPS unit provides.
         self.GPRMC = self.parse_GPRMC(NMEAdata) # Turn a GPRMC sentence into a Python dictionary called gpsData
         if self.GPRMC['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
            if self.FirstFixFlag is False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
               self.FirstFixDate = self.GPRMC['fix_date'] + "-" + self.GPRMC['fix_time']
               self.FirstFixFlag = True
            else: # write the data to a simple log file and then the raw data as well:
               if DEBUG == True:print self.GPRMC
               #print(self.GPRMC['fix_date'] + "," + self.GPRMC['fix_time'] + "," + str(self.GPRMC['decimal_latitude']) + "," + str(self.GPRMC['decimal_longitude']) +"\n")
               '''
               with open("/home/pi/MySkipper/" + self.FirstFixDate +"-simple-log.txt", "a") as myfile:
                  myfile.write(self.GPRMC['fix_date'] + "," + self.GPRMC['fix_time'] + "," + str(self.GPRMC['decimal_latitude']) + "," + str(self.GPRMC['decimal_longitude']) +"\n")
               with open("/home/pi/MySkipper/" + self.FirstFixDate +"-gprmc-raw-log.txt", "a") as myfile:
                  myfile.write(line)
               '''
               pass


'''

FirstFixFlag = False # this will go true after the first GPS fix.
FirstFixDate = ""

# Set up serial:
SerialGPS = serial.Serial(
   port='/dev/ttyUSB0',\
   baudrate=4800,\
   parity=serial.PARITY_NONE,\
   stopbits=serial.STOPBITS_ONE,\
   bytesize=serial.EIGHTBITS,\
   timeout=1)

GPRMCdata = {
            'fix_time': '000000.000',
            'validity': 'A',
            'latitude': '0000.0000',
            'latitude_hemisphere' : 'N',
            'longitude' : '00000.0000',
            'longitude_hemisphere' : 'E',
            'speed': '0.00',
            'true_course': '000.00',
            'fix_date': '000000',
            'variation': '',
            'variation_e_w' : '',
            'checksum' : ''
}

#------------------------------------------------
# Initialisation
def Init():
   pass
#------------------------------------------------
# Helper function to take HHMM.SS, Hemisphere and make it decimal
def degrees_to_decimal(data, hemisphere):
   try:
      decimalPointPosition = data.index('.')
      degrees = float(data[:decimalPointPosition-2])
      minutes = float(data[decimalPointPosition-2:])/60
      output = degrees + minutes
      if hemisphere is 'N' or hemisphere is 'E':
         return output
      if hemisphere is 'S' or hemisphere is 'W':
         return -output
   except:
      return ""

#------------------------------------------------
# Helper function to take a $GPRMC sentence, and turn it into a Python dictionary.
# This also calls degrees_to_decimal and stores the decimal values as well.
def parse_GPRMC(data):
   data = data.split(',')
   GPRMC = {
            'fix_time': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_hemisphere' : data[4],
            'longitude' : data[5],
            'longitude_hemisphere' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'fix_date': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
   }
   GPRMC['decimal_latitude'] = degrees_to_decimal(GPRMC['latitude'], GPRMC['latitude_hemisphere'])
   GPRMC['decimal_longitude'] = degrees_to_decimal(GPRMC['longitude'], GPRMC['longitude_hemisphere'])
   return GPRMC

#------------------------------------------------
# Main program loop
def Communicate():
   global FirstFixFlag,FirstFixDate
   global GPRMCdata

   NMEAdata = SerialGPS.readline()
   print NMEAdata
   if "$GPRMC" in NMEAdata: # This will exclude other NMEA sentences the GPS unit provides.
      GPRMCdata = parse_GPRMC(NMEAdata) # Turn a GPRMC sentence into a Python dictionary called gpsData
      if GPRMCdata['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
         if FirstFixFlag is False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
            FirstFixDate = GPRMCdata['fix_date'] + "-" + GPRMCdata['fix_time']
            FirstFixFlag = True
         else: # write the data to a simple log file and then the raw data as well:
            print GPRMCdata
            return GPRMCdata
#             with open("/home/pi/MySkipper/" + FirstFixDate +"-simple-log.txt", "a") as myfile:
#                myfile.write(GPRMCdata['fix_date'] + "," + GPRMCdata['fix_time'] + "," + str(GPRMCdata['decimal_latitude']) + "," + str(GPRMCData['decimal_longitude']) +"\n")
#             with open("/home/pi/MySkipper/" + FirstFixDate +"-gprmc-raw-log.txt", "a") as myfile:
#                myfile.write(line)
'''