#!/usr/bin/python

import time
from dbf import dbf
import cfgreader as cfg
#import datetime
import RPi.GPIO as GPIO

import os, sys
fpid = os.fork()
if fpid!=0:
  # Running as daemon now. PID is fpid
  sys.exit(0)

# Configuration
__hyst = 1.0
__heatpin = 26

config_file = '/etc/heatcontroll.xml'
config = cfg.parsecofig(config_file)

db = dbf()
db.init(config_file)

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
GPIO.setwarnings(False)
GPIO.setup(__heatpin, GPIO.OUT)  # set up pin
GPIO.output(__heatpin,GPIO.LOW)

def getIsDay():
    hour = (int(time.strftime('%H')) +2) % 24
    if(hour >= 7 and hour <= 23 ):
        return True
    return False

def setHeat(value):
#    print "Set heater {}".format(value)
    GPIO.output(__heatpin,value)
    db.SetControllValue("heating","feedback",value)

def checkTemperature():
    last = db.GetLastValue("in")
    act_temp = last[3]
    if (time.time() - time.mktime(last[0].timetuple()) > 600):
        return False

    heat_on = int(db.GetControllValue("heating","onoff"))
    if (heat_on == None):
        return False

    if (heat_on == 0):
        setHeat(GPIO.LOW)
        return True

    if getIsDay():
        daynight = "temp"
    else:
        daynight = "temp_night"

    heat_temp = float(db.GetControllValue("heating",daynight))
#    print "{} : {} : {}".format(heat_on, heat_temp, act_temp)
    if(heat_temp - __hyst > act_temp):
        setHeat(GPIO.HIGH)
        return True

    if(heat_temp + __hyst < act_temp):
        setHeat(GPIO.LOW)
        return True

while(True):
   time.sleep( 15 )
   checkTemperature()



GPIO.cleanup(__heatpin)
