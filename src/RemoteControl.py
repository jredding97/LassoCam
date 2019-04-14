import time
from serial import Serial

class RemoteControl:

    def __init__(self, dev_name):
        self.conn = Serial(dev_name)

    def hasWaiting(self):
        if self.conn.inWaiting() > 0:
            return True
        else:
            return False

    def read(self):
        readIn = self.conn.readline()
        line = readIn.rstrip()
        return int(line)
