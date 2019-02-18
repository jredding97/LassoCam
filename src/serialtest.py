import serial
ser = serial.Serial("/dev/rfcomm0", baudrate = 9600)
while 1:
    print(ser.readline())
    print("Reading again")