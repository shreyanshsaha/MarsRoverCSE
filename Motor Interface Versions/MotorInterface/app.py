from flask import Flask, render_template, request, jsonify
import serial

from motor import Motor
from compass import Compass
from roverGps import RoverGps
import math
from math import pi as PI
app = Flask(__name__)

# ================
# Global Variables
# ================
motorPath = "/dev/ttyACM0"
gpsErr = 'None'
motorConnected=False

nextLocation = dict({})
currentLocation = dict({})
nextGpsLat = None
nextGpsLon = None

# ================
# Connecting Motor
# ================
try:
	roverMotor = Motor(motorPath)
	motorConnected=True
except serial.serialutil.SerialException:
	motorConnected = False

gps = RoverGps()
compass = Compass("/dev/ttyACM1")

# ================
# Helper Functions
# ================
def resetMotor(roverMotor):
	global motorConnected
	try:
		roverMotor.connectMotor(motorPath)
		motorConnected=True
	except serial.serialutil.SerialException:
		motorConnected = False

def getSlope(currentLocation):
	global nextLocation
	n1 = float(currentLocation['lat'])
	e1 = float(currentLocation['lon'])
	
	n2 = float(nextLocation['lat'])
	e2 = float(nextLocation['lon'])
	try:
		slope = math.atan((n2-n1)/(e2-e1))*180/PI
		if e2-e1 < 0:
			slope = 180 + slope
		
	except ZeroDivisionError:
		return "\n\nDivide by 0"

	return int(90-slope)

# ======
# Routes
# ======
@app.route('/')
def renderHome():
	return render_template('index.html')
		
@app.route("/setMotors", methods=["GET"])
def runMotors():
	global roverMotor
	if not motorConnected:
		return "Error: Motor not connected!"
	try:
		if request.args.get('reset'):
			resetMotor(roverMotor)
			return "Reset!"
		if request.args['front']=='true':
			roverMotor.moveMotor('forward')
			return "Forward"
		elif request.args['right']=='true':
			roverMotor.moveMotor('right')
			return "Right"
		elif request.args['back']=='true':
			roverMotor.moveMotor('back')
			return "Backward"
		elif request.args['left']=='true':
			roverMotor.moveMotor('left')
			return "Left"
		elif request.args['stop']=='true':
			roverMotor.moveMotor('stop')
			return "Stopped!"
		elif request.args['gearup']=='true':
			return "Motor Speed: "+str(roverMotor.incrementRPM())
		elif request.args['geardown']=='true':
			return "Motor Speed: "+str(roverMotor.decrementRPM())
		else:
			return "Error: Unknown Command!"
	except KeyError:
		roverMotor.moveMotor('stop')
		return "Error: Unknown Key!"
	
@app.route("/setRPM/<int:value>", methods=["GET"])
def setRPM(value):
	global roverMotor
	if value>255:
		return "Error: Invalid value range!"
	roverMotor.setRPM(value)
	return "Success!"

@app.route("/getGps")
def returnGpsValue():
	global gpsErr, currentLocation
	if gpsErr=='None':
		report = gps.getGpsData()

		currentLocation['lon']=report[0]
		currentLocation['lat']=report[1]

		if currentLocation['lat'] == None:
			currentLocation['lat'] = 'Null'
		if currentLocation['lon'] == None:
			currentLocation['lon'] = 'Null'
	return jsonify(
		currentLocationLat=currentLocation['lat'],
		currentLocationLon=currentLocation['lon'],
		# gpsError=gpsErr
		)
@app.route("/getCompass")
def returnCompassValue():
	global nextLocation
	compassValueRequired='None'
	if len(nextLocation)>0:
		compassValueRequired = getSlope(currentLocation)

	return jsonify(compassValue=compass.getCompassAngle(), compassValueRequired=compassValueRequired)

@app.route("/setNextLocation", methods=["GET"])
def setNextLocation():
	global nextLocation
	nextLocation = {'lat':request.args.get('lat'), 'lon':request.args.get('lon'),}
	print(nextLocation)
	return jsonify(nextLocation)

# ===================
# Running application
# ===================
app.debug = True
app.run('',port=5000, debug=True)