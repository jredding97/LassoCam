from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2

class ObjectTracker:

	presenterBB = None
	laserBB = None
	tracker_name = "csrt"
	tracker = None
	frame = None
	info = None
	
			
	def tracker_dict(self, tracker_name):
		OPENCV_OBJECT_TRACKERS = {
			"csrt": cv2.TrackerCSRT_create,
			"kcf": cv2.TrackerKCF_create,
			"boosting": cv2.TrackerBoosting_create,
			"mil": cv2.TrackerMIL_create,
			"tld": cv2.TrackerTLD_create,
			"medianflow": cv2.TrackerMedianFlow_create,
			"mosse": cv2.TrackerMOSSE_create
		}
		
		return OPENCV_OBJECT_TRACKERS[tracker_name]	
	

	def __init__(self):
		
		self.tracker = cv2.TrackerCSRT_create()
		self.video_stream = VideoStream(src=0).start()
		print("Using OpenCV version " + cv2.__version__ + "\n")

	
	def setTracker(self, tracker_name):
		self.tracker_name = tracker_name
		self.tracker = self.tracker_dict(tracker_name)
		
	def update_presenter(self, frame):
		self.frame = frame
		
		# If the feed is done, do not update
		if frame is None:
			return
		
		# Resize frame and grab frame dimensions
		frame = imutils.resize(frame, width=500)
		(H, W) = frame.shape[:2]
	
		# Are we currently tracking?
		if self.presenterBB is not None:
		
			# Grab bounding box coordinate of object
			(success, box) = self.tracker.update(self.frame)
			
			# Successful?
			if success:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				return box
				
	def set_presenter(self, initBB):
		self.presenterBB = initBB
		print(initBB)
		self.tracker.init(self.frame, initBB)

	def get_presenter(self):
		return self.presenterBB
	
	def release_webcam(self):
		self.video_stream.stop()