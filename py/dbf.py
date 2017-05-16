import MySQLdb
import cfgreader
#because of scatter
#from plotly.graph_objs import *

class dbf:

    cursor = False
    db = False

    # Read configuration file
    def init(self, config_file):
        config = cfgreader.parsecofig(config_file)
        db_host = cfgreader.getvalue(config, "db/host")
        db_user = cfgreader.getvalue(config, "db/username")
        db_pass = cfgreader.getvalue(config, "db/password")
        db_name = cfgreader.getvalue(config, "db/name")

        self.db = MySQLdb.connect(db_host,db_user,db_pass,db_name )
        self.cursor = self.db.cursor()

    def InsertSensorValue(self, date, val, sensor):
        if (val <= 0.0):
            return False

        q="INSERT INTO temp_sensors (time, sensor, readinterval, val) VALUES ('{}','{}', 'min', '{:.2f}');".format(date, sensor, val)
        try:
            self.cursor.execute(q)
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format(str(e))
            print q

    def ReadScatterData(self, sensor, df, dt, interval):
#        from plotly.graph_objs import *
#        import plotly.graph_reference
        from plotly.graph_objs import Scatter

        try:
            self.cursor.execute("select time, sensor, val from temp_sensors s1 where readinterval = '{}' AND time >= '{}' AND time < '{}' AND sensor = '{}'".format(interval, df, dt, sensor))
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format( str(e))
            print q
            return False
        trace = Scatter(
            x=[],
            y=[]
        )
        for i in self.cursor.fetchall():
            trace.x.append(i[0])
            trace.y.append(float(i[2]))
        return trace

    def commit(self):
        self.db.commit()

    def GetSensors(self):
        q="SELECT distinct sensor FROM temp_sensors;"
        try:
            self.cursor.execute(q)
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format(str(e))
            print q
        sensors = []
        for i in self.cursor.fetchall():
            sensors.append(i[0])
        return sensors

    def GetAvg(self, sensor, t, interval):
        import time
        gmt = time.gmtime(t)
        tstart = t - gmt.tm_sec
        if(interval >= 3600):
            tstart = tstart - (gmt.tm_min * 60)
        if(interval >= 86400):
            tstart = tstart - (gmt.tm_hour * 3600)


        ftimef = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(tstart))
        ftimet = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(tstart + interval))

#        ftimef = time.strftime("%Y-%m-%d %H:00:00",t)
#        ftimef = time.strftime("%Y-%m-%d %H:00:00",t)
#        ftimet = time.strftime("%Y-%m-%d %H:59:59",t)


        q="SELECT AVG(val) from temp_sensors WHERE readinterval = 'min' AND sensor = '{}' AND time > '{}' AND time < '{}';".format(sensor, ftimef, ftimet)
#        q="SELECT AVG(val) FROM temp_sensors WHERE sensor = '{}';".format(sensor, time, time)
#        print q
        try:
            self.cursor.execute(q)
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format( str(e))
            print q
            return False
        avg = self.cursor.fetchone()[0]
        if avg != None:
#          print t
          ftimem = time.strftime("%Y-%m-%d %H:30:00",time.gmtime(t))
          q="INSERT INTO temp_sensors (time, sensor, readinterval, val) VALUES ('{}','{}', 'hour', '{:.2f}');".format(ftimem, sensor, avg)
#          print q
#          return
        try:
            self.cursor.execute(q)
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format(str(e))
            print q
#         " w() - interval 1 hour, '%Y-%c-%d %H:00:00');"
#        q="INSERT INTO temp_sensors (time - interval 30 minutes)"

    def close(self):
        self.db.close()
