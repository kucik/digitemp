import time
from dbf import dbf
import cfgreader as cfg
import os
os.environ["TZ"]="Europe/Prague"
goback_time = 20*60
t_remove_delay = 60*60*24 * 7

# Configuration
config_file = '../cfg/config.xml'
config = cfg.parsecofig(config_file)

db = dbf()
db.init(config_file)

t = time.time() - goback_time

s = db.GetSensors()
for i in s:
#    print i
    db.GetAvg(i, t, 3600)

# clean old records
t_remove = time.time() - t_remove_delay
db.RemoveOldData(t_remove)

db.commit()
