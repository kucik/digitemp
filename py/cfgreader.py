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




# Configuration
#config_file = '../cfg/config.xml'

#cfg = parsecofig(config_file)


#for child in cfg.iterfind('sensors/sensor'):
#   print child.iterfind('id').next().text
#   print child.iterfind('name').next().text
#   print child.iterfind('device').next().text
