import tkinter as Tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source_1=0, video_source_2=0):
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title(window_title)
        self.video_source_1 = video_source_1
        self.video_source_2 = video_source_2

        # open video source (the webcam for now)
        self.video1 = ImageCapture(self.video_source_1)
        self.video2 = ImageCapture(self.video_source_2)

        # make a canvas
        self.canvas = Tkinter.Canvas(window, width=480, height=540)
        self.canvas.pack()

        # make a message area
        self.message = Tkinter.Label(window, text="This is where instructions go for the user!", bg="red", fg="white")
        self.message.pack()

        # make a button
        self.button = Tkinter.Button(window, text= "Calibrate")
        self.button.pack()

        # updates every self.delay number of milliseconds
        self.delay = 250
        self.update()

        self.window.mainloop()

 	# used to update the canvas with the current video frame
    def update(self):
        ret, frame = self.video1.get_frame()
        if ret:
            self.pic = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.pic, anchor=Tkinter.NW)

        ret2, frame2 = self.video2.get_frame()
        if ret2:
            self.pic2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
            self.canvas.create_image(0, 270, image=self.pic2, anchor=Tkinter.NW)

        self.window.after(self.delay, self.update)


class ImageCapture:
    def __init__(self, video_source_1=0, video_source_2=0):
        # open the video source
        self.video1 = cv2.VideoCapture(video_source_1)
        if not self.video1.isOpened():
            raise ValueError("can't find video source 1", video_source_1)

        self.video2 = cv2.VideoCapture(video_source_2)
        if not self.video2.isOpened():
            raise ValueError("can't find video source 2", video_source_2)

    def get_frame(self):
        if self.video1.isOpened():
            ret, frame = self.video1.read()
            if ret:
              	# resize the current frame to fit nicely
                frame = cv2.resize(frame, (0,0), fx=0.38, fy=0.38)
                # return the frame using BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

        if self.video2.isOpened():
            ret2, frame2 = self.video2.read()
            if ret2:
              	# resize the current frame to fit nicely
                frame2 = cv2.resize(frame2, (0,0), fx=0.38, fy=0.38)
                # return the frame using BGR
                return (ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
            else:
                return (ret2, None)
        else:
            return (ret2, None)

# create a window for the app
App(Tkinter.Tk(), "LassoZoom Calibration GUI")
