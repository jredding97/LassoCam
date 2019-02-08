# import statements
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument(
	"-v", "--video", type=str, help="path to input video file"
)
ap.add_argument(
	"-t", "--tracker", type=str, default="kcf", help="OpenCV object tracker type"
)

args = vars(ap.parse_args())

# Get OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]

# If we are using OpenCV 3.2 OR BEFORE, we can use special factory
# function to generate an object tracker
if int(major) == 3 and int(minor) < 3:
	tracker = cv2.Tracker_create(args["tracker"].upper())
	
# Otherwise, for OpenCV 3.3 OR NEWER, we need to explicitly call the
# appropriate object tracker constructor
else:
	# Dictionary of function mappings
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}
	
	# Use arg to generate correct tracker
	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
	
# Initialize bounding box coordinates of object
initBB = None

# If no video path, grab reference to web cam
if not args.get("video", False):
	print("[INFO] Starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
	
# Otherwise grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
	
# initialize the FPS throughput estimator
fps = None

# Loop over videostream frames
while True:
	# Grab frame, handle
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
	
	# Check to see if end of stream
	if frame is None:
		break
		
	# Resize frame and grab frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]
	
	# Are we currently tracking?
	if initBB is not None:
		# Grab bounding box coordinate of object
		(success, box) = tracker.update(frame)
		
		# Successful?
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
		#Update FPS
		fps.update()
		fps.stop()
		
		# Initialize set of information we'll be displaying on the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		
		# Loop over the info tuples and draw them on frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			
	# Show output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	# If the 's' key is selected, select a bounding box
	if key == ord("s"):
		# select bounding box (Press Enter or Space after selection
		initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
		
		# Initialize tracker/FPS
		tracker.init(frame, initBB)
		fps = FPS().start()
		
	# If the 'q' key is pressed, break loop
	elif key == ord("q"):
		break

# If we are using a webcam, release pointer
if not args.get("video", False):
	vs.stop()
	
# Release file pointer
else:
	vs.release()
	
#Close all
cv2.destroyAllWindows()
			
