import socket

HOST = 'localhost'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
#videofile = "yeet.txt"
#bytes = open(videofile).read()
sendStr = "Ocean man, take me by the hand lead me to the land (that you understand)."
print(len(sendStr))
#print (len(bytes))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

client.send(sendStr)

client.close()
