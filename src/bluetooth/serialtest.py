import serial

ser = serial.Serial("/dev/rfcomm1")
while True:
    if ser.inWaiting() > 0:
        print(ser.readline())
