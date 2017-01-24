import MySQLdb
from datetime import datetime
import xml.etree.ElementTree as ET
import plotly.plotly as py
from plotly.graph_objs import *

# Configuration
config_file = '../cfg/config.xml'

def log(p):
    print p

##
# Get text field text identified by pattern 'column' in xmltree 'tree'
def getvalue( tree, column ):
    try:
        val = tree.iterfind(column).next()
        return val.text
    except:
        return ""



# Read configuration file
config = ET.parse(config_file)
db_host = getvalue(config, "db/host")
db_user = getvalue(config, "db/username")
db_pass = getvalue(config, "db/password")
db_name = getvalue(config, "db/name")

db = MySQLdb.connect(db_host,db_user,db_pass,db_name )
cursor = db.cursor()
df = "2016-09-10 00:00:00"
dt = "2016-09-12 00:00:00"

#cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '2016-11-07 00:00:00' AND")
#cursor.execute("select s1.time, s1.sensor, s1.val from temp_sensors s1, temp_sensors s2 where s1.time >= '2015-11-17 00:00:00' AND s1.time < '2015-11-18 00:00:00' s1.sensor='s1' AND s2.sensor='s2' AND s1.tim = s2.time")

#dates = list()
#vals = list()
#for i in cursor.fetchall():
#    dates.append(i[0])
#    vals.append(float(i[2]))
s="s1"
cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '{}' AND time < '{}' AND sensor = '{}'".format(df, dt, s))

trace0 = Scatter(
  x=[],
  y=[]
)
for i in cursor.fetchall():
    trace0.x.append(i[0])
    trace0.y.append(float(i[2]))

s="s2"
cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '{}' AND time < '{}' AND sensor = '{}'".format(df, dt, s))
trace1 = Scatter(
  x=[],
  y=[]
)
for i in cursor.fetchall():
    trace1.x.append(i[0])
    trace1.y.append(float(i[2]))



s="s3"
cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '{}' AND time < '{}' AND sensor = '{}'".format(df, dt, s))
trace2 = Scatter(
  x=[],
  y=[]
)
for i in cursor.fetchall():
    trace2.x.append(i[0])
    trace2.y.append(float(i[2]))


data = Data([trace0, trace1, trace2 ])
py.plot(data, filename = 'test3', auto_open=False)

# disconnect from server
db.close()
