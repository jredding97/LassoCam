from tkinter import *
from tkinter import ttk, filedialog
import cv2
from time import sleep
import imutils
import os
import datetime
import numpy as np
from threading import Thread, Lock
from picamera.array import PiRGBArray
from picamera import PiCamera
from ObjectTracker import ObjectTracker
from CameraControl import CameraControl
from imutils.video import VideoStream, FPS

#globals from GUI
global stage
stage = 0
global directory
directory = None
global distance
distance = 0

global displayMap
displayMap = False
global mapFrame
mapFrame = None
global initBB
initBB = None
global selectROI
selectROI = False

#GUI creation
class GUI:
    def __init__(self, app, tracking_source):

        self.app = app

        # window
        self.window = Tk()
        self.window.title("LassoCam Setup")
        self.window.geometry('250x350')

        # progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.bar = ttk.Progressbar(self.window, length=250, style='black.Horizontal.TProgressbar')
        self.bar['value'] = 0
        self.bar.grid(column=0, row=0)

        # labels
        self.lbl1 = Label(self.window, text="LassoCam", font=("Arial Bold", 14))
        self.lbl1.grid(column=0, row=1)
        self.lbl2 = Label(self.window, text="Welcome to the LassoCam\ncamera calibration program\nclick continue to proceed", font=("Arial Italic", 14))
        self.lbl2.grid(column=0, row=2, pady=(100,0))

        # text entry
        self.txt = Entry(self.window,width=10)

        # button
        self.btn = Button(self.window, text="Continue", command=self.next_stage)
        self.btn.grid(column=0, row=4, pady=(90,10))

        
        while True:
            global mapFrame
            global displayMap
            global initBB
            global selectROI
            if displayMap is True:
                cv2.imshow("Frame", mapFrame)
                cv2.waitKey(1) & 0xFF

            if selectROI is True:
                initBB = cv2.selectROI("Select Presenter", mapFrame, fromCenter=False, showCrosshair=True)
                cv2.destroyWindow("Select Presenter")
                self.app.select_presenter()
                self.app.start_tracker()
                selectROI = False

            self.window.update_idletasks()
            self.window.update()




        # run window
 
    #GUI mapping
    def next_stage(self):
        global directory
        global distance
        global stage 
        stage = stage + 1
        if stage == 1:
            self.bar['value'] = 20 
            self.lbl1.configure(text="Setup Camera")
            self.lbl2.configure(text="Place the camera so the\nentire stage is shown,\nthen click continue")
            self.txt.grid_forget()

            # Display map camera
            self.app.start_map()
        elif stage == 2:
            self.bar['value'] = 40
            self.lbl1.configure(text="Measuring Distance")
            self.lbl2.configure(text="Enter the distance (in inches)\nfrom the camera to the stage,\nthen click continue")
            self.txt.grid(column=0, row=3)
            self.txt.focus()
            self.btn.grid(column=0, row=4, pady=(61,10))
        elif stage == 3:
            self.bar['value'] = 60
            distance = int(self.txt.get())
            self.app.camControl.calibrate(distance, 0)
            self.lbl1.configure(text="Person Selection")
            self.lbl2.configure(text="Select the torso of the\nperson you'd like to track,\nthen click continue")
            self.btn.grid(column=0, row=4, pady=(90,10))
            self.txt.grid_forget()

            # Select Presenter
            global selectROI
            selectROI = True

        elif stage == 4:
            self.bar['value'] = 80
            self.lbl1.configure(text="Save Destination")
            self.lbl2.configure(text="Choose where to save the video\nafter it has been recorded,\nthen click continue")
            self.btn.grid(column=0, row=4, pady=(90,10))
            directory = filedialog.askdirectory()
            self.lbl2.configure(text=directory)
            self.btn.grid(column=0, row=4, pady=(122,10))
        elif stage == 5:
            self.bar['value'] = 100
            self.lbl1.configure(text="Begin Recording")
            self.lbl2.configure(text="Click the button to exit setup\nand immediately begin recording\nusing LassoCam technology")
            self.btn.configure(text="Start", command=self.next_stage)
            self.btn.grid(column=0, row=4, pady=(90,10))

        elif stage == 6:
            self.app.start_recording('video.h264')
            self.bar['value'] = 100
            self.lbl1.configure(text="Begin Recording")
            self.lbl2.configure(text="Click the button to stop recording")
            self.btn.configure(text="Stop", command=self.next_stage)
            self.btn.grid(column=0, row=4, pady=(90,10))

        else:
            self.app.stop_recording()
            displayMap = False
            print(" ")
            print("--- SETUP OVER ---")
            print(directory)
            print(distance)
            print(" ")
            self.window.quit()

class CamFeed:
    def __init__(self):
        # Open the video source
        self.cap = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.cap.read()
        self.read_lock = Lock()

        self.stopped = False
        self.t = Thread(target=self.update_frame, name="camUpdate", args=())
        self.t.daemon = True
        self.t.start()

    def get_frame(self):

        self.read_lock.acquire()
        output = self.frame.copy()
        self.read_lock.release()
        output = imutils.resize(output, width=500)
        return output

    def update_frame(self):
        while self.stopped is False:
            (grabbed, frame) = self.cap.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def stop(self):
        self.stopped = True
        self.t.join()

    def __del__(self):
        self.stopped = True
        self.cap.release()


class App:

    def __init__(self):

        self.stopMap = False 
        self.stopTrack = False
        self.laserBB = None

        # Create Webcam Feed
        self.webCam = CamFeed()
        frame = self.webCam.get_frame()
        (self.fH, self.fW) = frame.shape[:2]

        self.piCam = PiCamera()

        # Create Object Tracker
        self.objectTracker = ObjectTracker("csrt")
        print("Object Tracker Created")

        # Create Camera Controller
        self.camControl = CameraControl()
        print("Camera Control Created")

        self.camControl.set_size(self.fH, self.fW)
        print("Distance: " + str(distance))

        #self.presenterBB = presenterBB
        #print("Presenter: " + str(presenterBB[0]) + ", " + str(presenterBB[1]))

        # Create GUI
        self.gui = GUI(self, 0)

        print("DisplayMap: " + str(displayMap))

    def start_map(self):

        # Create thread for map display
        tmap = Thread(target = self.update_map, name = "MapFeed Display", args=())
        tmap.daemon = True
        self.stopMap = False

        # Start thread
        tmap.start()

        sleep(0.5)

        global displayMap
        displayMap = True

        return self

    def stop_map(self):
        self.stopMap = True

    def select_presenter(self):
        global initBB
        global mapFrame
        self.objectTracker.set_presenter(mapFrame, initBB)
        self.objectTracker.update_presenter(mapFrame)

    def start_tracker(self):
        # Create thread for tracking
        tTrack = Thread(target = self.update_tracker, name = "Tracker Thread", args=())
        tTrack.daemon = True

        # Start thread
        tTrack.start()

        return self

    def start_pantilt(self):
        # Create thread for pantilt
        tPantilt = Thread(target = self.update_pantilt, name = "Pantilt Thread", args=())
        tPantilt.daemon = True

        # Start thread
        tPantilt.start()

        return self

    def start_recording(self, path):
        self.piCam.resolution = (640, 480)
        self.piCam.framerate = 30
        self.piCam.vflip = True
        self.piCam.start_recording('video.h264')

    def stop_recording(self):
        self.piCam.stop_recording()

    def detect(self):
        # Create thread for pantilt
        tDetector = Thread(target = self.update_detector, name = "Detector Thread", args=())
        tDetector.daemon = True

        # Start thread
        tDetector.start()

        return self

    def update_tracker(self):
        global mapFrame
        while True:
            self.objectTracker.update_presenter(mapFrame)
            xCoord, yCoord = self.objectTracker.get_presenter()
            print("updated to: " + str(xCoord) + ", " + str(yCoord))
            self.camControl.set_angle(xCoord, yCoord)

    def update_map(self):
        global mapFrame
        while self.stopMap is False:
            # Grab frame, show it
            mapFrame = self.webCam.get_frame()
            sleep(0.03)

    def update_pantilt(self):
        while True:
            if not self.stopPantilt:
                # Grab coordinates
                self.camControl.set_angle(self.x, self.y)

    def update_detector(self):

        print()




# Grab devices
#roiwc = cv2.VideoCapture(1)

#ret, frame = roiwc.read()

#frame = imutils.resize(frame, width=500)

#height, width = frame.shape[:2]

#cv2.namedWindow("Select Presenter")
#presenterBB = cv2.selectROI("Select Presenter", frame, fromCenter=False, showCrosshair=True)

#cv2.destroyAllWindows()
#roiwc.release()

#wc = VideoStream(src=1)
#pc = VideoStream(usePiCamera=True)

# Open application
App()
print("Past app")


