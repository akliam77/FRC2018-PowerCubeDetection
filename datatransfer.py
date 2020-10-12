from networktables import NetworkTables as nt

class DataTransfer(object):

    def __init__(self):
        self.ip = "10.46.82.2"
        self.sd = nt.getTable("SmartDashboard")
        self.sc = nt.getTable("Scale")
        self.s = nt.getTable("Switch")
    
    def valueChanged(self, table, key, value, isNew):
        print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key,value, isNew))

    def connectionListener(self, connected, info):
        print(info, '; connected=%s' % connected)