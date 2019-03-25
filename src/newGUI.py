from Tkinter import *
import tkFileDialog
from ttk import Progressbar
import ttk

global stage
stage = 0

global directory
directory = None

global distance
distance = 0

def next_stage():
	global directory
	global distance
	global stage 
	stage = stage + 1
	if stage == 1:
		bar['value'] = 20 
		lbl1.configure(text="Setup Camera")
		lbl2.configure(text="Place the camera so the\nentire stage is shown,\nthen click continue")
		txt.grid_forget()
	elif stage == 2:
		bar['value'] = 40
		lbl1.configure(text="Measuring Distance")
		lbl2.configure(text="Enter the distance (in feet)\nfrom the camera to the stage,\nthen click continue")
		txt.grid(column=0, row=3)
		txt.focus()
		btn.grid(column=0, row=4, pady=(61,10))
	elif stage == 3:
		bar['value'] = 60
		distance = int(txt.get())
		lbl1.configure(text="Person Selection")
		lbl2.configure(text="Select the torso of the\nperson you'd like to track,\nthen click continue")
		btn.grid(column=0, row=4, pady=(90,10))
		txt.grid_forget()
	elif stage == 4:
		bar['value'] = 80
		lbl1.configure(text="Save Destination")
		lbl2.configure(text="Choose where to save the video\nafter it has been recorded,\nthen click continue")
		btn.grid(column=0, row=4, pady=(90,10))
		directory = tkFileDialog.askdirectory()
		lbl2.configure(text=directory)
		btn.grid(column=0, row=4, pady=(122,10))
	elif stage == 5:
		bar['value'] = 100
		lbl1.configure(text="Begin Recording")
		lbl2.configure(text="Click the button to exit setup\nand immediately begin recording\nusing LassoCam technology")
		btn.configure(text="Start", command=next_stage)
		btn.grid(column=0, row=4, pady=(90,10))
	else:
		print(" ")
		print("--- SETUP OVER ---")
		print(directory)
		print(distance)
		print(" ")
		window.quit()

window = Tk()
window.title("LassoCam Setup")
window.geometry('250x350')

style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=250, style='black.Horizontal.TProgressbar')
bar['value'] = 0
bar.grid(column=0, row=0)
 
lbl1 = Label(window, text="LassoCam", font=("Arial Bold", 14))
lbl1.grid(column=0, row=1)

lbl2 = Label(window, text="Welcome to the LassoCam\ncamera calibration program\nclick continue to proceed", font=("Arial Italic", 14))
lbl2.grid(column=0, row=2, pady=(100,0))

txt = Entry(window,width=10)

btn = Button(window, text="Continue", command=next_stage)
btn.grid(column=0, row=4, pady=(90,10))

window.mainloop()