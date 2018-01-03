import cfgreader as cfg
import sensor
import time
from dbf import dbf
import os

# Configuration
config_file = '../cfg/config.xml'

config = cfg.Configuration(config_file)

#timezone setup
os.environ["TZ"]= config.getvalue('TimeZone')

def readSensors():
    for sensorc in config.iterfind('sensors/sensor'):
        sid = cfg.getvalue(sensorc, 'id')
        name = cfg.getvalue(sensorc, 'name')
        device = cfg.getvalue(sensorc, 'device')

        temp = sensor.read_temp(device)
        if temp:
            print "{} {} = {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), name, temp)
            db.InsertSensorValue(time.strftime("%Y-%m-%d %H:%M:00"), temp, sid)
            db.commit();
#            db.insertdata()


db = dbf()
db.init(config_file)

readSensors()

db.close()
