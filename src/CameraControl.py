import time
from pantilthat import pan, tilt
from picamera import PiCamera
import math
from random import randint
from datetime import datetime


class CameraControl:
    piCam = PiCamera()

    def __init__(self):
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


    def get_angle(self, xCoord, yCoord):
        xAngle = self.calc_angle(xCoord, self.xDist, self.distance, x=True)
        yAngle = self.calc_angle(yCoord, self.yDist, self.distance, x=False)
        self.curAngleX = xAngle
        self.curAngleY = yAngle
        self.curX = xCoord
        self.curY = yCoord

        return (xAngle, yAngle)

    def set_angle(self, xCoord, yCoord):
        # Calculate angle via coordinates
        xAngle, yAngle = self.get_angle(xCoord, yCoord)

        pan(xAngle)
        tilt(yAngle)

        # Camera should only be corrected if more than 2 degrees off
        if abs(xAngle - self.curAngleX) > 2 or abs(yAngle - self.curAngleY) > 2:
            # Point camera to position
            print()

	def get_zoom(self, yBound, xBound):
		zoomX = (self.halfX * 2)/(xBound * 3)
		gridX = zoom / 2.0
		zoomy = (self.halfY * 2)/(yBound * 3)
		gridy = zoom / 2.0
		return (gridX, gridY, zoomX,zoomY)
		
    def start_recording(self, path):
        self.piCam.resolution = (640, 480)
        self.piCam.framerate = 30
        self.piCam.vflip = True

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
        filename = 'LassoCam - ' + currDT.strftime("%Y%m%d-%H%M%S") + '.h264'
        return (path + '/' + filename)

    def set_size(self, h, w):
        self.fH = h
        self.fW = w
        self.halfX = w/2
        self.halfY = h/2

    def calc_angle(self, coord, dist, distance, x):
        if x is True:
            #figure out which side we're on/where we're going
            if coord >= self.halfX:
                n = coord - self.halfX
                angle = math.degrees(math.atan((dist * n / 1900) / distance)) * -1
                return angle
            else:
                n = self.halfX - coord
                angle = math.degrees(math.atan((dist * n / 1900) / distance))
                return angle
        else:
            #figure out which side we're on/where we're going
            if coord >= self.halfY:
                n = coord - self.halfY
                angle = math.degrees(math.atan((dist * n / 1900) / distance)) * -1
                return angle
            else:
                n = self.halfY - coord
                angle = math.degrees(math.atan((dist * n / 1900) / distance))
                return angle

#newCam = CameraControl()
#newCam.calibrate(120, 50)
#print(newCam.get_angle(1900,1080))

