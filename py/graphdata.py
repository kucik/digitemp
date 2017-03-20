#import MySQLdb
#from datetime import datetime
#import xml.etree.ElementTree as ET
import sys
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

data = Data([])

i=0
t = time.gmtime(time.time() - (24 * 60 * 60))
trace1 = db.ReadScatterData("in", time.strftime("%Y-%m-%d %H:%M:%S",t),  time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time.time())), 'min')
#print 'trace read'

# viz ./python2.7/dist-packages/plotly/graph_objs/graph_objs.py

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
