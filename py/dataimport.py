import MySQLdb
from datetime import datetime
import xml.etree.ElementTree as ET

# Configuration
config_file = '../cfg/config.xml'

def log(p):
    print p

##
# Get text field text identified by pattern 'column' in xmltree 'tree'
def getvalue( tree, column ):
    try:
        val = tree.iterfind(column).next()
#        print val.text
        return val.text
    except:
#        print "cannot iterate through"+ column
        return ""

def safecast(mystr):
    try:
        n=float(mystr)
    except:
        n=0.0
    return n

def createInsert(date, val, sensor):
    if (val <= 0.0):
        return False

    q="INSERT INTO temp_sensors (time, sensor, readinterval, val) VALUES ('{}','{}', 'sec', '{:.2f}');".format(date, sensor, val)
    try:
        cursor.execute(q)
    except MySQLdb.Error, e:
        log( "MySQL Error: %s" % str(e))
        log(q)

####################################
## Main script
####################################

# Read configuration file
config = ET.parse(config_file)
db_host = getvalue(config, "db/host")
db_user = getvalue(config, "db/username")
db_pass = getvalue(config, "db/password")
db_name = getvalue(config, "db/name")

db = MySQLdb.connect(db_host,db_user,db_pass,db_name )
cursor = db.cursor()

ln=0
datafile="../logs/sensors.log.temp.2"
f = open(datafile)
for line in f:
    data=line.split()
    date=data[0]+" "+data[1]
    s1=safecast(data[2])
    s2=safecast(data[3])
    s3=safecast(data[4])
#    if ( s3 > 0.0 ) :
#        print 'date:{} s1:{} s2:{} s3:{}'.format(date, s1, s2, s3)
#        print "date:"+date+" s1:"+s1+" s2:"+s2+" s3:"+s3
    createInsert(date, s1, "s1")
    createInsert(date, s2, "s2")
    createInsert(date, s3, "s3")
    ln+=1;
    if ( (ln % 1000) == 0):
        print "{} Insert {}: {}, {}, {};".format(ln, date, s1, s2, s3)


db.commit()

# disconnect from server
db.close()
