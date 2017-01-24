import MySQLdb
from datetime import datetime
import xml.etree.ElementTree as ET
import plotly.plotly as py
from plotly.graph_objs import *


#from plotly import __version__
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#print __version__

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

def CreateScatter( sensor, df, dt):
    try:
        cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '{}' AND time < '{}' AND sensor = '{}'".format(df, dt, sensor))
    except MySQLdb.Error, e:
        log( "MySQL Error: %s" % str(e))
        log(q)
        return False
    trace = Scatter(
        x=[],
        y=[]
    )
    for i in cursor.fetchall():
        trace.x.append(i[0])
        trace.y.append(float(i[2]))
    return trace

# Read configuration file
config = ET.parse(config_file)
db_host = getvalue(config, "db/host")
db_user = getvalue(config, "db/username")
db_pass = getvalue(config, "db/password")
db_name = getvalue(config, "db/name")

db = MySQLdb.connect(db_host,db_user,db_pass,db_name )
cursor = db.cursor()
df = "2016-09-10 00:00:00"
dt = "2016-09-17 00:00:00"

#cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '2016-11-07 00:00:00' AND")
#cursor.execute("select s1.time, s1.sensor, s1.val from temp_sensors s1, temp_sensors s2 where s1.time >= '2015-11-17 00:00:00' AND s1.time < '2015-11-18 00:00:00' s1.sensor='s1' AND s2.sensor='s2' AND s1.tim = s2.time")

#dates = list()
#vals = list()
#for i in cursor.fetchall():
#    dates.append(i[0])
#    vals.append(float(i[2]))

trace0 = CreateScatter("s1", df, dt)
trace1 = CreateScatter("s2", df, dt)
trace2 = CreateScatter("s3", df, dt)

data = Data([trace0, trace1, trace2 ])
#data = Data([trace0 ])
py.plot(data, filename = 'test3', auto_open=False)
#iplot(data, filename = 'test3')

# disconnect from server
db.close()
