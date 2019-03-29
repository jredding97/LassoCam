from tkinter import *
from tkinter import ttk
import cv2
from time import sleep
import imutils
import os
import datetime
from threading import Thread
#from picamera.array import PiRGBArray
#from picamera import PiCamera
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

        # run window
        self.window.mainloop()
 
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
            self.lbl1.configure(text="Person Selection")
            self.lbl2.configure(text="Select the torso of the\nperson you'd like to track,\nthen click continue")
            self.btn.grid(column=0, row=4, pady=(90,10))
            self.txt.grid_forget()
            sleep(0.5)

            # Select Presenter
            self.app.select_presenter()
            self.app.start_tracker()
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
        else:
            print(" ")
            print("--- SETUP OVER ---")
            print(directory)
            print(distance)
            print(" ")
            self.window.quit()

class CamFeed:
    def __init__(self, cap):
        # Open the video source
        self.cap = cap
        cap.start()

    def get_frame(self):

        frame = self.cap.read()

        if not frame is None:
            # resize the current frame
            frame = imutils.resize(frame, width=300)
            return frame

        # If any part fails, return None
        return None

    def __del__(self):
        self.cap.stop()


class App:

    def __init__(self, webcam, picam):

        self.stopMap = False 
        self.stopTrack = False

        # Create Webcam Feed
        self.webCam = CamFeed(webcam)
        print("Opened webcam")

        # Create PiCam Feed
        self.piCam = CamFeed(picam)
        print("opened piCam")

        # Create Object Tracker
        self.objectTracker = ObjectTracker("kcf")

        # Create Camera Controller
        self.camControl = CameraControl(picam)

        # Create GUI
        self.gui = GUI(self, 0)


    def start_map(self):
        # Create thread for map display

        tmap = Thread(target = self.update, name = "MapFeed Display", args=())
        tmap.daemon = True
        tmap.start()

        return self

    def stop_map(self):
        self.stopMap = True

    def select_presenter(self):
        initBB = cv2.selectROI(self.webCam.get_frame(), fromCenter=False, showCrosshair=True)
        self.objectTracker.set_presenter(initBB)
        self.objectTracker.update_presenter()

    def start_tracker(self):
        tTrack = Thread(target = self.objectTracker.update_presenter, name = "Tracker Thread", args=())
        tTrack.daemon = True
        tTrack.start()

        return self

    def update(self):
        while True:
            if not self.stopMap:
                # Grab frame, show it
                frame = self.webCam.get_frame()
                cv2.imshow("Frame", frame)
                cv2.waitKey(10) & 0xFF
                sleep(0.04)

# Grab devices
wc = VideoStream()
pc = VideoStream(usePiCamera=True)

# Open application
App(wc, pc)
