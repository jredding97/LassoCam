from picamera import PiCamera
import pantilthat
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.flip()

while True:
    pointer = -90
    pantilthat.tilt(-10)

    while pointer < 90:
        pantilthat.pan(pointer)
        sleep(0.05)
        pointer += 1

    while pointer > -90:
        pantilthat.pan(pointer)
        sleep(0.05)
        pointer -= 1

camera.stop_preview()
