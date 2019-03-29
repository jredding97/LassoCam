# import statements
from imutils.video import VideoStream
import imutils
import time
import cv2

classNames = {0: 'background', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

# Load model
print("[INFO] Loading model...")
net = cv2.dnn.readNetFromCaffe('../../resources/caffeMobilenet.prototxt', '../../resources/mobilenet.caffemodel')

print("Opening webcam")
cam = VideoStream(0).start()

while True:

    image = cam.read()
    image = imutils.resize(image, width=300)

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104, 117, 123))


    net.setInput(blob)
    output = net.forward()

    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        if confidence > 0.5:
            class_id = detection[1]
            class_name = id_class_name(class_id, classNames)
            box_x = detection[3] * w
            box_y = detection[4] * h
            box_w = detection[5] * w
            box_h = detection[6] * h
            cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_w), int(box_height)), (23, 230, 210), thickness=1)
            cv2.putText(image, class_name, (int(box_x), int(box_y+0.05*h)), cv2.FONT_HERSHEY_SIMPLEX,(0.005*w), (0, 0, 255))

    cv2.imshow('image', image)
    cv2.waitKey(0)
