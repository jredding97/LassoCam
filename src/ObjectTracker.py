from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2
from datetime import datetime

class ObjectTracker:
        def spawn_tracker(self, tracker_name):
                availableTrackers = {
                        "csrt": cv2.TrackerCSRT_create,
                        "kcf": cv2.TrackerKCF_create,
                        "boosting": cv2.TrackerBoosting_create,
                        "mil": cv2.TrackerMIL_create,
                        "tld": cv2.TrackerTLD_create,
                        "medianflow": cv2.TrackerMedianFlow_create,
                        "mosse": cv2.TrackerMOSSE_create
                }
                
                # spawner = availableTrackers[tracker_name]
                tracker = cv2.TrackerCSRT_create()
                return tracker
        
        def __init__(self, tracker_to_use="kcf"):
                self.presenterBB = None
                self.laserBB = None
                self.info = None
                self.tracker_name = tracker_to_use
                self.tracker = self.spawn_tracker(self.tracker_name)
                self.version = cv2.__version__

                # For performance, these are hard coded for a 16:9 ratio camera
                # Change to whatever aspect ratio is used, with width of 500
                self.frameHeight = 889
                self.frameWidth = 500

        def set_tracker(self, tracker_name):
                self.tracker_name = tracker_name
                self.tracker = self.spawn_tracker(tracker_name)
        
        def update_frame(self, frame):
                # If the feed is done, just set to None
                if frame is None:
                        frame = None

                # Otherwise, resize the image and update
                else:
                        frame = imutils.resize(frame, width=500)

        def update_presenter(self, frame):

                start = datetime.now()
                # If the feed is done, do not update
                if frame is None:
                        return

                # Are we currently tracking?
                if self.presenterBB is not None:
                
                        # Grab bounding box coordinate of object
                        (success, box) = self.tracker.update(frame)
                        
                        # Successful?
                        if success:
                            # print("Success")
                            self.presenterBB = box
                        else:
                            print("Lost you")

                end = datetime.now()
                print("Tracking took: " + str(end-start))
                                
        def set_presenter(self, frame, initBB):
                self.presenterBB = initBB
                print(self.presenterBB)
                self.tracker.init(frame, self.presenterBB)

        def get_presenter(self):
                return self.presenterBB
        
        def release_webcam(self):
                self.video_stream.stop()
