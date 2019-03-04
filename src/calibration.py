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
        print(os.getcwd())
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title(window_title)
		
        self.video_source_a = video_source_a
        self.video_source_b = video_source_b
		
        self.tracker_module = ObjectTracker()
 
        # open video source (the webcam for now)
        self.video_a = MyVideoCapture(self.video_source_a)
        self.video_b = MyVideoCapture(self.video_source_b)

        # make a canvas
        self.canvas = Tkinter.Canvas(window, width=888, height=1000)
        self.canvas.pack()
        
        # make a message area
        self.message = Tkinter.Label(window, text="This is where instructions go for the user!", bg="red", fg="white")
        self.message.pack()

        # make a Calibrate button
        self.btn_calibrate = Tkinter.Button(window, text="Calibrate")
        self.btn_calibrate.pack()
    
        # make a selection button
        self.btn_selection = Tkinter.Button(window, text="Make Selection")
        self.btn_selection.pack()

        # updates every self.delay number of milliseconds
        self.delay = 15
        self.update()
 
        self.window.mainloop()
 
    # used to update the canvas with the current video frame
    def update(self):
        ret_a, frame_a = self.video_a.get_frame()
        if ret_a:
            self.photo_a = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_a))
            self.canvas.create_image(0, 0, image = self.photo_a, anchor = Tkinter.NW)

        ret_b, frame_b = self.video_b.get_frame()
        if ret_b:
            box = self.tracker_module.update_presenter(frame_b)
            if not box is None:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.photo_b = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_b))
            self.canvas.create_image(0, 500, image = self.photo_b, anchor = Tkinter.NW)
            
        self.window.after(self.delay, self.update)
 
class MyVideoCapture:
    def __init__(self, video_source_a, video_source_b):
        # Open the video source
        self.cap_a = cv2.VideoCapture(video_source_a)
        if not self.cap_a.isOpened():
            raise ValueError("Unable to open video source", video_source_a)
            
        self.cap_b = cv2.VideoCapture(video_source_b)
        if not self.cap_b.isOpened():
            raise ValueError("Unable to open video source", video_source_b)
  
        # Get video source width and height
        self.width_a = self.cap_a.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height_a = self.cap_a.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        self.width_b = self.cap_b.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height_b = self.cap_b.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.cap_a.isOpened():
            ret_a, frame_a = self.cap_a.read()
            if ret_a:
                # resize the current frame to fit nicely
                frame_a = cv2.resize(frame_a, (0,0), fx=0.38, fy=0.38)
                # return the frame using BGR
                return (ret_a, cv2.cvtColor(frame_a, cv2.COLOR_BGR2RGB))
            else:
                return (ret_a, None)
        else:
            return (ret_a, None)

        if self.cap_b.isOpened():
            ret_b, frame_b = self.cap_b.read()
            if ret_b:
                # resize the current frame to fit nicely
                frame_b = cv2.resize(frame2, (0,0), fx=0.38, fy=0.38)
                # return the frame using BGR
                return (ret_b, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
            else:
                return (ret_b, None)
        else:
            return (ret_b, None)
            
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap_a.isOpened():
            self.cap_a.release()
            
        if self.cap_b.isOpened():
            self.cap_b.release()
 
# create a window for the app
App(Tkinter.Tk(), "LassoCam Calibration GUI", "../resources/eveMitochondria.mp4", "../resources/saveTheDrugs.mp4")
