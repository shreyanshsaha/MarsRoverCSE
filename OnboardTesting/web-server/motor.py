
#! Dont do redundant work
#! Already arduino code is writte
#! No need to use nanpy

import time
import serial

class Motor():
  def __init__(self, device):
    self.devicePath = device
    self.baudRate = 9600
    self.currentCommand = None
    # try:
    #   self.Arduino = serial.Serial(self.devicePath, self.baudRate)
    # except Exception as e:
    #   raise e

  def moveMotor(self, command):
    if command == self.currentCommand:
      print("Ignoring, same command")
    else:
      self.currentFunction=command
      if self.currentFunction=='zoomIn':
        data='i'
      elif self.currentFunction=='zoomOut':
        data='o'
      elif self.currentFunction=='left':
        data='a'
      elif self.currentFunction=='right':
        data='c'
      elif self.currentFunction=='pump1':
        data='1'
      elif self.currentFunction=='pump2':
        data='2'
      elif self.currentFunction=='stop':
        data='s'
      elif self.currentFunction=='reset':
        data='s'
      else:
        data=''
      # self.Arduino.write(bytes(data,'UTF-8'))