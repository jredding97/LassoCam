import time
import pantilthat
from picamera import PiCamera
import math
from random import randint
from datetime import datetime


class CameraControl:
    piCam = None

    def __init__(self, picam):
        self.piCam = picam
        #distance, in inches of the camera's FOV
        self.xDist = 0
        self.yDist = 0
        #camera's current angle
        self.curAngleX = 0
        self.curAngleY = 0
        #camera's current grid location
        self.curX = 950
        self.curY = 540
        #camera's distance from plane of interest
        self.distance = 0
        print()


    def get_angle(self, xCoord, yCoord):
        xAngle = calc_angle(1, xCoord, self.xDist, self.distance)
        yAngle = calc_angle(1, xCoord, self.yDist, self.distance)
        self.curAngleX = xAngle
        self.curAngleY = yAngle
        self.curX = xCoord
        self.curY = yCoord

        return (xAngle, yAngle)

    def set_angle(self, xCoord, yCoord):
        # Calculate angle via coordinates
        xAngle, yAngle = get_angle(xCoord, yCoord)

        # Point camera to position
        pantilthat.pan(xAngle)
        pantilthat.tilt(yAngle)


    def start_recording(self, path):
        filename = self.generate_filename(path)
        self.piCam.start_recording(filename)


    def stop_recording(self):
        self.piCam.stop_recording()


    def calibrate(self, distance, height):
        self.distance = distance
        self.height = height
        self.xDist = 2 * self.distance * math.tan(math.radians(35.21))
        self.yDist = 2 * self.distance * math.tan(math.radians(21.65))


    def generate_filename(self, path):
        currDT = datetime.now()
        filename = 'LassoCam - ' + currDT.strftime("%Y%m%d-%H%M%S")
        return (path + '\\' + filename)

def calc_angle(xy, coord, dist, distance):
    halfGrid = 0

    if xy == 1: #x
        halfGrid = 950
    else:       #y
        halfGrid = 540
    #figure out which side we're on/where we're going
    if coord >= halfGrid:
        n = coord - halfGrid
        angle = math.degrees(math.atan((dist * n / 1900) / distance))
        return angle
    else:
        n = halfGrid - coord
        angle = math.degrees(math.atan((dist * n / 1900) / distance)) * -1
        return angle

#newCam = CameraControl()
#newCam.calibrate(120, 50)
#print(newCam.get_angle(1900,1080))

