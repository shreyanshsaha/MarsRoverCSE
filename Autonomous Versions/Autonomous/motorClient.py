
#? This is the client motor file
#? It connects to th client and send info about how to move the motor
import time
import socket
from sys import exit

BUFFER = 512

class Motor():
  def __init__(self, addr):
    self.connectMotor(addr)
  
  def connectMotor(self, addr):
    try:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(addr)
    except ConnectionRefusedError:
      print("Server has not started!")
      exit(-1)

  def moveMotor(self, direction):
    if direction == 'forward':
      direction ='F'
    elif direction == 'backward':
      direction='B'
    elif direction=='left':
      direction='L'
    elif direction=='right':
      direction='R'
    elif direction == 'stop':
      direction='S'

    self.client.send(str(direction).encode('ascii'))