# from compass import Compass
from nanpy import ArduinoApi, SerialManager
import time
class Motor():
  def __init__(self, device):
    # self.compass = compassObject
    self.devicePath=device
    self.RPM=50
    self.rotateRPM=160
    self.currentDirection=None
    self.RPMOptions=[50, 100, 120, 150, 170, 200, 255]
    self.currentSpeed = 0
    # Directions
    self.m11 = 2
    self.m12 = 4
    self.m21 = 8
    self.m22 = 6

    # Speed
    self.s11 = 3
    self.s12 = 5
    self.s21 = 9
    self.s22 = 7

    self.connectMotor()
  
  def connectMotor(self):
    try:
      connection = SerialManager(self.devicePath) #CHANGE THIS
      self.motorSerial = ArduinoApi(connection=connection)
    except Exception as e:
      raise e
  
  def setRPM(self, value):
    self.RPM = value
    newDir = self.currentDirection
    self.currentDirection=''
    self.moveMotor(newDir)

  def incrementRPM(self):
    self.currentSpeed=self.currentSpeed+1
    if self.currentSpeed>len(self.RPMOptions)-1:
      self.currentSpeed=len(self.RPMOptions)-1
    self.setRPM(self.RPMOptions[self.currentSpeed])
    return self.RPMOptions[self.currentSpeed]

  def decrementRPM(self):
    self.currentSpeed=self.currentSpeed-1
    if self.currentSpeed<0:
      self.currentSpeed=0
    self.setRPM(self.RPMOptions[self.currentSpeed])
    return self.RPMOptions[self.currentSpeed]

  #* Motor Movements

  def moveMotor(self, direction):
    if direction == self.currentDirection:
      print("Ignoring, same direction")
    else:
      self.currentDirection=direction
      if self.currentDirection=='forward':
        self.forwardMotor()
      elif self.currentDirection=='backward':
        self.backwardMotor()
      elif self.currentDirection=='left':
        self.leftMotor()
      elif self.currentDirection=='right':
        self.rightMotor()
      elif self.currentDirection=='stop':
        self.resetAllMotors()

  def forwardMotor(self):
    print("Go forward!")
    self.motorSerial.analogWrite(self.s11,self.RPM)
    self.motorSerial.analogWrite(self.s12,self.RPM)
    self.motorSerial.analogWrite(self.s21,self.RPM)
    self.motorSerial.analogWrite(self.s22,self.RPM)
    
    self.motorSerial.digitalWrite(self.m11, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m12, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m21, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m22, self.motorSerial.LOW)

  def backwardMotor(self):
    self.motorSerial.analogWrite(self.s11,self.RPM)
    self.motorSerial.analogWrite(self.s12,self.RPM)
    self.motorSerial.analogWrite(self.s21,self.RPM)
    self.motorSerial.analogWrite(self.s22,self.RPM)
    
    self.motorSerial.digitalWrite(self.m11, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m12, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m21, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m22, self.motorSerial.HIGH)
  
  def leftMotor(self):
    self.motorSerial.analogWrite(self.s11,self.rotateRPM)
    self.motorSerial.analogWrite(self.s12,self.rotateRPM)
    self.motorSerial.analogWrite(self.s21,self.rotateRPM)
    self.motorSerial.analogWrite(self.s22,self.rotateRPM)
    
    self.motorSerial.digitalWrite(self.m11, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m12, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m21, self.motorSerial.HIGH)
    self.motorSerial.digitalWrite(self.m22, self.motorSerial.HIGH)

  def rightMotor(self):
    self.motorSerial.analogWrite(self.s11,self.rotateRPM)
    self.motorSerial.analogWrite(self.s12,self.rotateRPM)
    self.motorSerial.analogWrite(self.s21,self.rotateRPM)
    self.motorSerial.analogWrite(self.s22,self.rotateRPM)
    
    self.motorSerial.digitalWrite(self.m11, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m12, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m21, self.motorSerial.LOW)
    self.motorSerial.digitalWrite(self.m22, self.motorSerial.LOW)
  
  def resetAllMotors(self):
    self.motorSerial.analogWrite(self.s11,0)
    self.motorSerial.analogWrite(self.s12,0)
    self.motorSerial.analogWrite(self.s21,0)
    self.motorSerial.analogWrite(self.s22,0)
    
