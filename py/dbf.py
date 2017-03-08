import MySQLdb
import cfgreader
#because of scatter
from plotly.graph_objs import *

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

        q="INSERT INTO temp_sensors (time, sensor, readinterval, val) VALUES ('{}','{}', 'sec', '{:.2f}');".format(date, sensor, val)
        try:
            self.cursor.execute(q)
        except MySQLdb.Error, e:
            print "MySQL Error: {}".format(str(e))
            print q

    def ReadScatterData(self, sensor, df, dt):
        try:
            self.cursor.execute("select time, sensor, val from temp_sensors s1 where time >= '{}' AND time < '{}' AND sensor = '{}'".format(df, dt, sensor))
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


    def close(self):
        self.db.close()
