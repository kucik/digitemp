import time
from dbf import dbf
import cfgreader as cfg

# Configuration
config_file = '../cfg/config.xml'
config = cfg.parsecofig(config_file)

db = dbf()
db.init(config_file)

#t = time.gmtime(time.time() - (60 * 60))
t = time.time()
#q = 
#db.MakeAvg(sensor, time.strftime("%Y-%m-%d %H:00:00"))

s = db.GetSensors()
for i in s:
    print i
#    db.MakeAvg(i, time.strftime("%Y-%m-%d %H:00:00",t))
#    db.MakeAvg(i, t, 360)
    db.GetAvg(i, t, 360)

db.commit()

#db.MakeAvg("blbost", time.strftime("%Y-%m-%d %H:00:00",t)) 
#db.MakeAvg("blbost", t)
#trace1 = db.ReadScatterData("in", time.strftime("%Y-%m-%d %H:%M:%S",t),  time.strftime("%Y-%m-%d 23:59:59"))
#select avg(val) from temp_sensors where time > date_format(now() - interval 1 hour, '%Y-%c-%d %H:00:00');
