# TODO:
# 1. Figure out a way to check if gps is not connected

# ALGO:
# 1. Center the bot at north - Not needed anymore
# 2. Get the next Location slope
# 3. Rotate the bot that much angle
# 4. While the bot has not reached the location, move forward
# 5. If the bot is out of the slope angle, recenter it


# =======
# Imports
# =======
import numpy as np
import math
import os
from compass import Compass
from motor import Motor
from roverGps import RoverGps
from time import sleep
from math import pi as PI
from sys import exit

# =========
# Variables
# =========
nextLocationIndex=0
roverMotor=None			# Doesnt fucking work
compass=None
roverGps=None



# ======================
# Set locations to go to
# ======================

locations=[
	[12.842468, 80.155767],
	[12.842537, 80.155655],
	[12.842745, 80.155344],
	[12.842855, 80.156207]
]


# ================
# Helper Functions
# ================

# Returns the angle to move the rover to
# SLOPE CALCULATION IS PERFECT, DO NOT CHANGE IT
def getSlope(currentLocation):
	global nextLocationIndex
	global scaledLocations
	global locations
	n1 = currentLocation[0]
	e1 = currentLocation[1]
	
	n2 = locations[nextLocationIndex][0]
	e2 = locations[nextLocationIndex][1]
	try:
		slope = math.atan((n2-n1)/(e2-e1))*180/PI
		if e2-e1 < 0:
			slope = 180 + slope
		
	except ZeroDivisionError:
		print("\n\nDivide by 0")
		return
	# sleep(0.5)
	return 90-slope

# Function to move bot left or right according to the slope
# It returns true if rover is centered and false if rover is not centered
def centerBot(compass, getAngle, roverGps, roverMotor, threshold=0):
	
	currentLocation = roverGps.getGpsData()
	getAngle = getSlope(currentLocation)

	try:
		angle = compass.getCompassAngle()
	except ValueError as e:
		print("\nError: Inside centerBot: Calibrate Compass")
		return False
	try:
		if abs(abs(angle)-abs(getAngle))>threshold or np.sign(angle)!=np.sign(getAngle):
			print("Centering Rover!",currentLocation, locations[nextLocationIndex], end=": ")
			if(angle>getAngle):
				print("Rotate left ", getAngle, angle)
				roverMotor.moveMotor('left')
				# roverMotor.leftMotor()
			else:
				print("Rotate right ", getAngle, angle)
				roverMotor.moveMotor('right')
				# roverMotor.rightMotor()
			return False
		else:
			return True
	except TypeError:
		return False
	










# =============
# Main Function
# =============
def main():
	# Local functions in main function
	global nextLocationIndex
	global locations
	global roverMotor
	botCentered = False
	locationAccuracy=0.000005

	print("Setting devices...")
	compass = Compass("/dev/ttyACM0")
	roverMotor = Motor("/dev/ttyACM1")
	try:
		roverGps = RoverGps()
	except OSError:
		print("GPSD not started!")
		exit(-1)
	roverMotor.moveMotor('stop')
	print("All device set!")
	sleep(1)
	roverMotor.moveMotor('stop')
	# Set the bot to point at next location
	while not(170<compass.getCompassAngle() and compass.getCompassAngle()<180):
			print(compass.getCompassAngle())

		# os.system("clear")
	botCentered=False

	# Rotate Rover Once
	# angle = compass.getCompassAngle()-100
	# while compass.getCompassAngle()>angle or compass.getCompassAngle()<angle:
	# 	print("Calibration!")
	# 	roverMotor.moveMotor('left')
		
	roverMotor.moveMotor("stop")
	os.system("clear")
	print("Rover centered!")
	roverMotor.moveMotor('stop')
	sleep(2)
	# roverMotor.resetAllMotors()
	print("Locations:", locations)
	# input('Press anything to continue!')
	
	# =========
	# Main Loop
	# =========
	while nextLocationIndex < len(locations):
		# roverMotor.resetAllMotors()
		try:
			currentLocation = roverGps.getGpsData()
			# print(roverGps)
		except ValueError:
			print("GPS not set")
			continue
		if currentLocation[0]==None:
			print("GPS no location")
			continue
			
		if abs(currentLocation[0]-locations[nextLocationIndex][0])<locationAccuracy and  abs(currentLocation[1]-locations[nextLocationIndex][1])<locationAccuracy:
			roverMotor.moveMotor("stop")
			nextLocationIndex+=1
			if nextLocationIndex>=len(locations):
				break
			print(locations)
			print("Location Reached!", currentLocation)
			print("Press any key to continue")
			input()
			# sleep(2)
			# Center bot to north
			botCentered=False
			while not botCentered:
				# os.system("clear")
				
				if centerBot(compass, 0, roverGps, roverMotor, 20):
					print()
					botCentered=True
			botCentered=False
			print("Continue to location", locations[nextLocationIndex])
			sleep(1)
			# input()
			continue
		
		slope = getSlope(currentLocation)
		# Move the rover to this slope    
		while not botCentered:
			# os.system("clear")
			slope = getSlope(currentLocation)
			
			if centerBot(compass, slope, roverGps, roverMotor, 10):
				botCentered=True
			# sleep(0.5)
		if not centerBot(compass, slope, roverGps, roverMotor, 10):
			print()
			botCentered=False

		# # Move bot forward
		# # os.system("clear")
		try:
			print("Move Forward", roverGps.getGpsData(), locations[nextLocationIndex] ,slope, compass.getCompassAngle())
			# roverMotor.moveMotor('forward')
			roverMotor.moveMotor('forward')
		except ValueError:
			print("Compass Value error")
	roverMotor.moveMotor('stop')
	print("Finished!")

if __name__=="__main__":
	main()

