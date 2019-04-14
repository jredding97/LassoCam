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

        yAngle = math.degrees(math.atan(self.pixel_height * (yCoord - self.halfY) / float(self.distance)))

        return (xAngle, yAngle)

    def set_angle(self, xCoord, yCoord, boxWidth, boxHeight):
        start = datetime.now()
        # Calculate angle via coordinates
        center_x = xCoord + (boxWidth/2)
        center_y = yCoord + (boxHeight/3)
        xAngle, yAngle = self.get_angle(center_x, center_y)

        pan(xAngle)
        tilt(yAngle)
        end = datetime.now()
        print("Took " + str(end-start) + " to move.")

        self.piCam.zoom = self.get_zoom(boxWidth, boxHeight)


    def get_zoom(self, box_w, box_h):
        # ratio_x = box_w / float(640)
        # loc_x = ((640 - box_w) / float(2)) / float(640)
        ratio_x = (box_w / float(self.fW)) + .25
        if ratio_x > 1:
            ratio_x = 1
        loc_x = (1-ratio_x)/float(2)
        # print(str(ratio_x) + " @ " + str(loc_x))
        # ratio_y = self.aspect_ratio * ratio_x
        # loc_y = ((480 - box_h) / float(2)) / float(480)
        ratio_y = (self.aspect_ratio * ratio_x) + .25
        if ratio_y > 1:
            ratio_y = 1
        loc_y = (1-ratio_y)/float(2)
        # print(str(ratio_y) + " @ " + str(loc_y))
        print("Zoomed at: " + str(loc_x) + ", " + str(loc_y)
                + " to " + str(ratio_x) + "x" + str(ratio_y))
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
        filename = 'LassoCam_' + currDT.strftime("%Y-%m-%d_%H%M%S") + '.h264'
        return (path + '/' + filename)

    def set_size(self, h, w):
        self.fH = h
        self.fW = w
        self.halfX = w/2
        self.halfY = h/2
        self.aspect_ratio = h/w
