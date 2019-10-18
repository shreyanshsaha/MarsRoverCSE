# Import socket module 
# this is for both the analysis of picam_sent_frame and webcam_sent_frame
import socket
import numpy as np
import cv2 as cv
import time
import pickle

# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
PORT = 8002

count = 0

#Define codec and create video writer object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('test_feed_atbase.avi',fourcc,24,(848,480))  

# connect to the server on local computer 
s.connect(('192.168.0.172', PORT)) 
#change for pi - 192.168.0....
#for banka hotspot and self 192.168.43.191 
#for tp mars and self 192.168.0.123
# 172 on tp mars new pi
  
# receive data from the server
start = time.time()
while True:
    #actual = 1221120  # size to which linear array has to be enlarged
    #data = s.recv(1221120)
    # buffer is 1221120 since 848x480x3 values.
    #image = np.frombuffer(data, dtype = np.uint8)
    #print(image)
    #print(image.shape)
    #print(image.size)
    #apparent = image.size  # size of current received frame
    #print(data)
    #print(image[0:3])
    #extra = actual-apparent
    #if image.size<actual:
        #continue
    #image1 = np.pad(image(0,extra),'constant')
    #padding = np.zeros(extra,dtype='int')
    #print(padding)
    #image1 = np.append(image,np.zeros(1221120-len(image))).astype(np.uint8)
    #print(image1)
    #print(image1.size)
    #reshaping of linear to 3D
    #newImg = image.reshape((480,848,3))
    #print(newImg)
    #print(newImg.shape)
    try:
        count+=1
        #section to repair frame
        frame = s.recv(500000000)
        frame_arr = pickle.loads(frame)
        print('Received',repr(frame_arr))
        #cv.imwrite('feed.jpg',newImg)
        out.write(frame_arr)
        #print(count)
        if time.time()-start>10:
            break
        #break
    except pickle.UnpicklingError:
        continue
    


