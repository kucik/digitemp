#import MySQLdb
#from datetime import datetime
#import xml.etree.ElementTree as ET
import time
print "start"
import plotly.plotly as py
from plotly.graph_objs import *
from plotly import tools

from dbf import dbf
import cfgreader as cfg
print "init"

# Configuration
config_file = '../cfg/config.xml'
config = cfg.parsecofig(config_file)

db = dbf()
db.init(config_file)

#db = MySQLdb.connect(db_host,db_user,db_pass,db_name )
#cursor = db.cursor()
df = "2016-09-10 00:00:00"
dt = "2016-09-17 00:00:00"
#print "db init"
data = Data([])

i=0
t = time.gmtime(time.time() - (24 * 60 * 60))
trace1 = db.ReadScatterData("in", time.strftime("%Y-%m-%d %H:%M:%S",t),  time.strftime("%Y-%m-%d 23:59:59"))
#print 'trace read'

trace1.type = "scatter"
trace1.fill = "tozeroy"

data = Data([trace1],
)
#data = Data([trace0, trace1, trace2 ])
py.plot(data, filename = 'digitemp-day', auto_open=False)
#iplot(data, filename = 'test3')
#print "plot it"
# disconnect from server
db.close()
