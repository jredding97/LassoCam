from time import sleep
import RPi.GPIO
import picamera
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)

# to get this working on a pi, enter the following commands
# sudo pip install RPi.GPIO
# sudo pip install picamera

#secondly, you need to know what channel the camera is attached to.
#once you have this number, fill it in where comments demand a channel number
#and everything SHOULD work... hopefully


class MainCamera():

	def __init__(self):
		self.xRes = 1900
		self.yRes = 1080
		self.xAngle = 0
		self.yAngle = 0

	def setXAngle(self, newAngle):
		self.xAngle = newAngle

	def setYAngle(self, newAngle):
		self.yAngle = newAngle

def setServoAngle(camera, servo, angle):

	# pwm = GPIO.PWM(channel, frequency)
	pwm = RPi.GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

	#ADD ACTUAL CHANNEL NUMBERS HERE
	if servo == 0:
		camera.setXAngle(angle)
	elif servo == 1:
		camera.setYAngle(angle)
	else:
		print("INVALID SERVO ANGLE USED")



def setNewZoom(xCord, yCord, zoomPercent):

    with picamera.PiCamera() as camera:
        camera.resolution = (1900, 1080)
        camera.start_preview()
        newX = xCord / 1900
        newY = yCord / 1080
        camera.zoom = (newX, newY, zoomPercent, zoomPercent)

if __name__ == '__main__':
	import sys

	newCam = MainCamera()
	print(newCam.xAngle)

	#
	#servo = add here: channel number
	#RPi.GPIO.setup(servo, RPi.GPIO.OUT)
	#setServoAngle(newCam, servo, 30)

	print(newCam.xAngle)

	RPi.GPIO.cleanup()