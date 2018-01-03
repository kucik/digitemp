import xml.etree.ElementTree as ET

##
# Get text field text identified by pattern 'column' in xmltree 'tree'
def getvalue( tree, column ):
    try:
        val = tree.iterfind(column).next()
        return val.text
    except:
        return ""

def parsecofig(config_file):
    return ET.parse(config_file)


class Configuration():
    __remoteAdresses = dict()
    def __init__(self, config_file):
        self.tree = ET.parse(config_file)
        self.__readRemoteSesors()

    def __getRemoteSensorAdresses(self):
        return None
    def iterfind(self, column):
        return self.tree.iterfind(column)

    def getvalue( self, column):
        try:
           val = self.tree.iterfind(column).next()
           return val.text
        except:
           return ""
    def __readRemoteSesors(self):
        remote = self.tree.iterfind("RemoteSensors").next()
        for sensor in list(remote):
            s = dict()
            s['adress'] = getvalue(sensor, "adress")
            s['name'] = getvalue(sensor, "name")
            s['id'] = getvalue(sensor, "id")
            self.__remoteAdresses[s['adress']] = s

    def getSesorByAdress(self, adress):
        return self.__remoteAdresses[adress]


# Configuration
#config_file = '../cfg/config.xml'

#cfg = parsecofig(config_file)


#for child in cfg.iterfind('sensors/sensor'):
#   print child.iterfind('id').next().text
#   print child.iterfind('name').next().text
#   print child.iterfind('device').next().text
