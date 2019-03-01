import socket

HOST = '10.0.0.188'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
#videofile = "yeet.txt"
#bytes = open(videofile).read()
sendStr = "Ocean man, take me by the hand lead me to the land (that you understand)."
print(len(sendStr))
#print (len(bytes))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDR)

    s.sendall(b'ocean man, take me by the hand lead me to the land')
    data = s.recv(4096)
