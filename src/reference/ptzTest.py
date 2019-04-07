import time
from pantilthat import pan, tilt
from random import randint

while True:
        pan(randint(-90, 90))
        tilt(randint(-90, 90))
        time.sleep(1)
