from Tkinter import *
import tkFileDialog
from ttk import Progressbar
import ttk
import cv2
import time
import imutils
import os
import datetime
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#from ObjectTracker import ObjectTracker
#from CameraControl import CameraControl
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
	def __init__(self, tracking_source):
		# tracking modules
		#self.tracking_source = tracking_source
		#self.tracker_module = ObjectTracker("kcf")
		#self.camera_b = CameraFeed(self.tracking_source)
		# picam
        #self.picam = PiCamera()
        #self.camera_a = PiRGBArray(self.picam)
        #self.picam.resolution=(736, 416)

		# window
		self.window = Tk()
		self.window.title("LassoCam Setup")
		self.window.geometry('250x350')
		# progress bar
		style = ttk.Style()
		style.theme_use('default')
		style.configure("black.Horizontal.TProgressbar", background='black')
		self.bar = Progressbar(self.window, length=250, style='black.Horizontal.TProgressbar')
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
		elif stage == 4:
			self.bar['value'] = 80
			self.lbl1.configure(text="Save Destination")
			self.lbl2.configure(text="Choose where to save the video\nafter it has been recorded,\nthen click continue")
			self.btn.grid(column=0, row=4, pady=(90,10))
			directory = tkFileDialog.askdirectory()
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

#create GUI
GUI(0)
