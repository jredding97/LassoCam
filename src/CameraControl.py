import time
from pantilthat import pan, tilt
from picamera import PiCamera
import math
from random import randint
from datetime import datetime


class CameraControl:

    def __init__(self):
        self.piCam = PiCamera()

        #distance, in inches of the camera's FOV
        self.map_width = 0
        self.map_height = 0

        #camera's distance from plane of interest
        self.distance = 0


    def get_angle(self, xCoord, yCoord):
        xAngle = 0
        yAngle = 0

        #if xCoord >= self.halfX:
        xAngle = math.degrees(math.atan(self.pixel_width * (self.halfX - xCoord) / float(self.distance)))
        print(str(xAngle))
        #else:
        #    xAngle = math.degrees(math.atan((self.xDist * (self.halfX - xCoord) / self.fW) / self.distance))

        #if yCoord >= self.halfY:
        yAngle = math.degrees(math.atan(self.pixel_height * (yCoord - self.halfY) / float(self.distance)))
        print(str(yAngle))
        #else:
        #    yAngle = math.degrees(math.atan((self.yDist * (self.halfY - yCoord) / self.fW) / self.distance)) * -1

        return (xAngle, yAngle)

    def set_angle(self, xCoord, yCoord, boxWidth, boxHeight):
        # Calculate angle via coordinates
        center_x = xCoord + (boxWidth/2)
        center_y = yCoord + (boxHeight/3)
        xAngle, yAngle = self.get_angle(center_x, center_y)

        pan(xAngle)
        tilt(yAngle)

        self.piCam.zoom = self.get_zoom(boxWidth, boxHeight)

    def get_zoom(self, box_w, box_h):
        ratio_x = ((box_w * 3.0) / (640.0))
        loc_x = ((640 - box_w) / 2.0)/640
        print(str(ratio_x) + " @ " + str(loc_x))
        ratio_y = self.aspect_ratio * ratio_x
        # zoomy = (self.fH)/(box_h * 3)
        loc_y = ((480 - box_h) / 2.0)/480
        print(str(ratio_y) + " @ " + str(loc_y))
        return (loc_x, loc_y, ratio_x, ratio_y)
		
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
        self.map_width = 2 * self.distance * math.tan(math.radians(35.21))
        self.map_height = 2 * self.distance * math.tan(math.radians(21.65))
        self.pixel_width = self.map_width / float(self.fW)
        self.pixel_height = self.map_width / float(self.fH)


    def generate_filename(self, path):
        currDT = datetime.now()
        filename = 'Output-LassoCam-' + currDT.strftime("%Y%m%d-%H%M%S") + '.h264'
        return (path + '/' + filename)

    def set_size(self, h, w):
        self.fH = h
        self.fW = w
        self.halfX = w/2
        self.halfY = h/2
        self.aspect_ratio = h/w
#
#    def calc_angle(self, coord, dist, distance, x):
#        if x is True:
#            #figure out which side we're on/where we're going
#            if coord >= self.halfX:
#                n = coord - self.halfX
#                angle = math.degrees(math.atan((dist * n / self.fW) / distance)) * -1
#                return angle
#            else:
#                n = self.halfX - coord
#                angle = math.degrees(math.atan((dist * n / self.fW) / distance))
#                return angle
#        else:
 #           #figure out which side we're on/where we're going
  #          if coord >= self.halfY:
   #             n = coord - self.halfY
    #            angle = math.degrees(math.atan((dist * n / self.fH) / distance))
     #           return angle
      #      else:
       #         n = self.halfY - coord
        #        angle = math.degrees(math.atan((dist * n / self.fH) / distance)) * -1
         #       return angle
