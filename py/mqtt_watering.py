#!/usr/bin/python

from cfgreader import Configuration as cfg
import cfgreader
import paho.mqtt.client as paho
import time
import sys
from dbf import dbf

# Configuration
config_file = '/etc/heatcontroll.xml'
config = cfg(config_file)


#timezone setup
#import os
#os.environ["TZ"]= config.getvalue('TimeZone')

#db = dbf()
#db.init(config_file)



if len(sys.argv) < 2:
    sleeptime = 60*5
else:
    sleeptime = int(sys.argv[1])

client = paho.Client()
mqtt_pwd = cfgreader.getvalue(config.tree, "mqtt/password")
mqtt_username = cfgreader.getvalue(config.tree, "mqtt/username")
mqtt_host = cfgreader.getvalue(config.tree, "mqtt/host")
mqtt_topic = cfgreader.getvalue(config.tree, "mqtt/topic")

client.username_pw_set(mqtt_username,mqtt_pwd)
client.connect(mqtt_host)
client.loop_start()

client.publish("controll/pump", "1", qos=1)
#print("pump on. Wait {}".format(sleeptime))
time.sleep(sleeptime)
client.publish("controll/pump", "0", qos=1)
#print("pump off")


