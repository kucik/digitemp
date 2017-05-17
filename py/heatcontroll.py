#!/usr/bin/python

import time
from dbf import dbf
import cfgreader as cfg
#import datetime
import RPi.GPIO as GPIO


# Configuration
__hyst = 2.0
__heatpin = 21

config_file = '/etc/heatcontroll.xml'
config = cfg.parsecofig(config_file)

db = dbf()
db.init(config_file)

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
GPIO.setup(__heatpin, GPIO.OUT)  # set up pin
GPIO.output(__heatpin,GPIO.LOW)

def setHeat(value):
#    print "Set heater {}".format(value)
    GPIO.output(__heatpin,value)

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

    heat_temp = float(db.GetControllValue("heating","temp"))
#    print "{} : {} : {}".format(heat_on, heat_temp, act_temp)
    if(heat_temp - __hyst > act_temp):
        setHeat(GPIO.HIGH)
        return True

    if(heat_temp + __hyst < act_temp):
        setHeat(GPIO.LOW)
        return True

while(True):
   time.sleep( 5 )
   checkTemperature()



GPIO.cleanup(__heatpin)
