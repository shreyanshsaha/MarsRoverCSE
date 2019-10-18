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
