import time
import pantilthat
from random import randint
from datetime import datetime

class CameraControl:

    distance = None
    # height = None
    piCam = None

    def __init__(self):
        self.piCam = PiCamera()
        print()

    def get_angle(self, xCoord, yCoord):
        # Hard code webcam dimensions as 1920x1080 for now
        xPos = xCoord / 1920 
        yPos = yCoord / 1080 

        calculate angle
        print()

    def set_angle(self):
        print()

    def start_recording(self, path):
        filename = self.generate_filename(path)
        self.piCam.start_recording(filename)

    def stop_recording(self):
        self.piCam.stop_recording()
    
    def calibrate(self, distance, height):
        self.distance = distance
        self.height = height

    def generate_filename(self, path):
        currDT = datetime.now()
        filename = 'LassoCam - ' + currDT.strftime("%Y%m%d-%H%M%S")
        return (path + '\\' + filename)

