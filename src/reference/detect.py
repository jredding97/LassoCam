# import statements
from imutils.video import VideoStream
import imutils
import time
import cv2

classNames = {1 : 'laser', 2 : 'lasernot'}

def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

# Load model
print("[INFO] Loading model...")
# net = cv2.dnn.readNetFromTensorflow('../../resources/tflite_graph.pb', '../../resources/tflite_graph.pbtxt')
# net = cv2.dnn.readNetFromTensorflow('../../resources/saved_model.pb', '../../resource/graph.pbtxt')
net = cv2.dnn.readNetFromTensorflow('../../local/optimized.pb', '../../local/optimized.pbtxt')

print("Opening webcam")
cam = VideoStream(0).start()

while True:

    image = cam.read()
    image = imutils.resize(image, width=300)

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), size=(300, 300), swapRB=True, crop=False)

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
            cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_w), int(box_h)), (23, 230, 210), thickness=1)
            cv2.putText(image, class_name, (int(box_x), int(box_y+0.05*h)), cv2.FONT_HERSHEY_SIMPLEX,(0.005*w), (0, 0, 255))

    cv2.imshow('image', image)
    cv2.waitKey(1) & 0xFF
