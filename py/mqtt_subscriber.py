#!/usr/bin/python

from cfgreader import Configuration as cfg
import cfgreader
import sensor
import time
from dbf import dbf

#deamonize
import os, sys
fpid = os.fork()
if fpid!=0:
    # Running as daemon now. PID is fpid
    sys.exit(0)

# Configuration
config_file = '/etc/heatcontroll.xml'
config = cfg(config_file)


s = config.getSesorByAdress("289e0c65080000a9")

db = dbf()
db.init(config_file)

import paho.mqtt.client as paho
import time

def on_subscribe(client, userdata, mid, granted_qos):
    print("c: {} mid: {} data: {} pos: {}".format(client, mid, userdata, granted_qos))

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    adress = msg.topic.split('/')[-1]
    s = config.getSesorByAdress(adress)
    #print s
    db.InsertSensorValue(time.strftime("%Y-%m-%d %H:%M:00"), float(msg.payload), s['id'])
    db.commit();

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message

mqtt_pwd = cfgreader.getvalue(config.tree, "mqtt/password")
mqtt_username = cfgreader.getvalue(config.tree, "mqtt/username")
mqtt_host = cfgreader.getvalue(config.tree, "mqtt/host")
mqtt_topic = cfgreader.getvalue(config.tree, "mqtt/topic")

client.username_pw_set(mqtt_username,mqtt_pwd)
client.connect(mqtt_host)
client.subscribe(mqtt_topic, qos=1)

client.loop_forever()
