import tkinter as Tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import imutils
import os
from ObjectTracker import ObjectTracker
from CameraControl import CameraControl
from imutils.video import VideoStream
from imutils.video import FPS

 
class App:
    def __init__(self, window, window_title, video_source_a=0, video_source_b=0):
        # Define GUI
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title(window_title)
        self.window.geometry("500x900")
        
        self.video_source_a = video_source_a
        self.video_source_b = video_source_b
        
        # Define Modules
        self.tracker_module = ObjectTracker("kcf")
        #self.control_module = ControlModule()
 
        # open video source (the webcam for now)
        self.camera_a = CameraFeed(self.video_source_a)
        self.camera_b = CameraFeed(self.video_source_b)

        # make a canvas
        self.canvas = Tkinter.Canvas(window, width=888, height=800)
        self.canvas.pack()
        
        # make a message area
        self.message = Tkinter.Label(window, text="This is where instructions go for the user!", bg="red", fg="white")
        self.message.pack()

        # make a Calibrate button
        self.btn_calibrate = Tkinter.Button(window, text="Calibrate")
        self.btn_calibrate.pack()
    
        # make a Selection button
        self.btn_selection = Tkinter.Button(window, text="Make Selection", command=self.select_presenter)
        self.btn_selection.pack()

        # updates every self.delay number of milliseconds
        self.delay = 5
        self.update_feeds()
 
        self.window.mainloop()
 
    # used to update the canvas with the current video frame
    def update_feeds(self):
        self.update_feed_a()
        self.update_feed_b()
        self.window.after(self.delay, self.update_feeds)
        
    def update_feed_a(self):
        ret, frame = self.camera_a.get_frame()
        if ret:
            self.photo_a = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo_a = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.photo_a))
            self.canvas.create_image(0, 0, image = self.photo_a, anchor = Tkinter.NW)

    def update_feed_b(self):
        ret, frame = self.camera_b.get_frame()
        if ret:
            self.tracker_module.update_frame(frame)
            box = self.tracker_module.update_presenter()

            if not box is None:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # self.canvas.create_rectangle(x+0, y+410, x+0+w, y+410+h)

            self.photo_b = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 410, image = self.photo_b, anchor = Tkinter.NW)

            if not box is None:
                self.canvas.create_rectangle(x+0, y+410, x+0+w, y+410+h)

    def select_presenter(self):
        # select bounding box (Press Enter or Space after selection
        initBB = cv2.selectROI(self.camera_b.get_frame()[1], fromCenter=False, showCrosshair=True)
        self.tracker_module.set_presenter(initBB)
        self.tracker_module.update_presenter()

    def set_distance(self):
        # Calibrate ControlModule
        self.calibrateWindow(self.master)
        self.btn_calibrate["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.btn_calibrate["state"] = "normal"
 
class CameraFeed:
    def __init__(self, video_source):
        # Open the video source
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # resize the current frame to fit nicely
                frame = cv2.resize(frame, (0,0), fx=0.38, fy=0.38)
                # return the frame using BGR
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
 


class calibrateWindow(object):
    def __init__(self,master):
        top=self.top = Tkinter.Toplevel(master)

        self.lblDistance = Tkinter.Label(top,text="Enter the distance from the board to the LassoCam")
        self.lblDistance.pack()
        self.entDistance = Tkinter.Entry(top)
        self.entDistance.pack()

        self.lblHeight = Tkinter.Label(top,text="Enter the distance from the floor to the LassoCam")
        self.lblHeight.pack()
        self.entHeight = Tkinter.Entry(top)
        self.entHeight.pack()
        
        self.btnOK = Tkinter.Button(top,text='Ok',command=self.cleanup)
        self.btnOK.pack()

    def cleanup(self):
        self.distance = self.entDistance.get()
        self.height = self.entHeight.get()
        self.top.destroy()

# create a window for the app
App(Tkinter.Tk(), "LassoCam Calibration GUI", "../resources/eveMitochondria.mp4", "../resources/eveMitochondria.mp4")
