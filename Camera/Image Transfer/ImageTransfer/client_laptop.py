# Import socket module
# this is for both the analysis of picam_sent_frame and webcam_sent_frame
import socket
import numpy as np
import time

s = socket.socket()

# Define the port on which you want to connect
PORT = 8001

# connect to the server on local computer
s.connect(('192.168.43.30', PORT))

# receive data from the server

while True:
    data = s.recv(921600)
    # buffer is 921600 since 640x480x3 values.
    image = np.frombuffer(data, dtype = np.uint8)
    print(image)
    print(image.shape)
    #print(data)
    print(image[0:3])
    newImg = image.reshape((480,640,3))
    print(newImg)
    time.sleep(1)

# close the connection
s.close()