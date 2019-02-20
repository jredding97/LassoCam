import time
import pantilthat
from random import randint


while True:
	x = randint(-90, 90)
	y = randint(-90, 90)

	pantilthat.pan(x)
	pantilthat.tilt(y)

	time.sleep(1)


