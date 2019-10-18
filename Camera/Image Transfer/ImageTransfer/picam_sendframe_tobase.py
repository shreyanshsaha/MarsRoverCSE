import picamera
import numpy as np
import socket
import time
import pickle


def send_frame_tobase():
    PORT = 8001

    s = socket.socket()
    s.bind(('',PORT))
    s.listen(5)
    print("Server is listening")
    c,addr = s.accept()
    print("Connected!")
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 24
        time.sleep(2) # give warmup time
        obj = np.empty((480,640,3), dtype = np.uint8)
        while True:
            try:
                camera.capture(obj,'rgb')
                frame_string = pickle.dumps(obj, protocol=3)
                c.send(frame_string)
                print(obj.shape)
                #c.send(str(obj).encode('ascii'))
            except BrokenPipeError:
                break
    #break
    #for original script remove frame_string statement
    


# PORT_AUTO = 8010

# sck = socket.socket()
# sck.connect(('192.168.0.199',PORT_AUTO))

while True:
    # command = sck.recv(4096)
    # command = command.decode
    # if command == 'start':
        # sck.close()
    send_frame_tobase()


