import picamera
import numpy as np
import socket
import time
import pickle

PORT = 8002

s = socket.socket()
s.bind(('',PORT))
print("Server started!")
s.listen(5)
c,addr = s.accept()
print("Connection accepted!")
with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    camera.framerate = 24
    time.sleep(2) # give warmup time
    obj = np.empty((480,640,3), dtype = np.uint8)
    while True:
        camera.capture(obj,'rgb')
        # print(obj.shape)
        # obj.flatten()
        # c.send(obj.toString())
        # time.sleep(2)

