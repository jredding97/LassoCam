import tkinter as Tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import imutils
import os

from imutils.video import VideoStream
from imutils.video import FPS
from ObjectTracker import ObjectTracker
 
class App:
    def __init__(self, window, window_title, video_source_a=0, video_source_b=0):
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title(window_title)
        self.window.geometry("500x900")
        
        self.video_source_a = video_source_a
        self.video_source_b = video_source_b
        
        self.tracker_module = ObjectTracker()
 
        # open video source (the webcam for now)
        self.video_a = MyVideoCapture(self.video_source_a)
        self.video_b = MyVideoCapture(self.video_source_b)

        # make a canvas
        self.canvas = Tkinter.Canvas(window, width=888, height=800)
        self.canvas.pack()
        
        # make a message area
        self.message = Tkinter.Label(window, text="This is where instructions go for the user!", bg="red", fg="white")
        self.message.pack()

        # make a Calibrate button
        self.btn_calibrate = Tkinter.Button(window, text="Calibrate")
        self.btn_calibrate.pack()
    
        # make a selection button
        self.btn_selection = Tkinter.Button(window, text="Make Selection", command=self.select_presenter)
        self.btn_selection.pack()

        # updates every self.delay number of milliseconds
        self.delay = 5
        self.update()
 
        self.window.mainloop()
 
    # used to update the canvas with the current video frame
    def update(self):
        ret_a, frame_a = self.video_a.get_frame()
        if ret_a:
            self.photo_a = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_a))
            self.canvas.create_image(0, 0, image = self.photo_a, anchor = Tkinter.NW)

        ret_b, frame_b = self.video_b.get_frame()
        raw_b = self.video_b.raw_frame()
        if ret_b:
            box = self.tracker_module.update_presenter(raw_b)
            if not box is None:
                (x, y, w, h) = [int(v) for v in box]
                print("Tracking subject at " + str(x) + ", " + str(y))
                cv2.rectangle(frame_b, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.photo_b = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_b))
            self.canvas.create_image(0, 410, image = self.photo_b, anchor = Tkinter.NW)
            if not box is None:
                self.canvas.create_rectangle(x+0, y+410, x+0+w, y+410+h)
            
        self.window.after(self.delay, self.update)
        
    def select_presenter(self):
        # select bounding box (Press Enter or Space after selection
        initBB = cv2.selectROI(self.video_b.raw_frame(), fromCenter=False, showCrosshair=True)
        self.tracker_module.set_presenter(initBB)
        self.tracker_module.update_presenter(self.video_b.raw_frame())
 
class MyVideoCapture:
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
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
            
    def raw_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # resize current frame to fit
                frame = cv2.resize(frame, (0,0), fx=0.38, fy=0.38)
                # return frame
                return frame
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
 
# create a window for the app
App(Tkinter.Tk(), "LassoCam Calibration GUI", "../resources/eveMitochondria.mp4", "../resources/eveMitochondria.mp4")
