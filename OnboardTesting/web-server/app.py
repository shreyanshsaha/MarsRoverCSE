import serial
import nanpy
import collections
from nanpy import ArduinoApi, SerialManager
from flask import Flask, render_template, request, jsonify

# Custom Packages
from motor import Motor
# import threading

# =========
# Variables
# =========
# Boolean Variables / Flags
isAuto = False
initialized = False
initializedNext=False
# Object initializations
arduino=None
soilMotors=None

# Variables regarding error
# textPastCommand='NoR' # !Remove this
err='None'
arduinoErr='None'
# Dictionary to store response
response = dict()


# Set up flask
app = Flask(__name__)
def connectSerial():
	global arduinoErr, arduino
	try:
		arduino=serial.Serial("/dev/ttyACM0", 9600)
		arduinoErr='None'
	except Exception as e:
		arduinoErr=str(e)
		response['serialError']=arduinoErr


# Initial Connection
# roverCompass = Compass()
soilMotors = Motor('/dev/ttyACM0')
connectSerial()

# Motor.digitalWrite(7, Motor.HIGH)
# ======
# Routes
# ======
@app.route("/")																			# Home page
def sendData():
	return render_template("main.html")

@app.route("/setMotors", methods=["GET"])
def runMotors():
	err='None'
	print(request.args)
	if request.args.get('reset'):
		soilMotors.moveMotor('reset')
		return "reset"

	if request.args['zoomIn']=='TRUE':
		soilMotors.moveMotor('zoomIn')
		return "zoomIn"
	elif request.args['turnRight']=='TRUE':
		soilMotors.moveMotor('right')
		return "right"
	elif request.args['zoomOut']=='TRUE':
		soilMotors.moveMotor('zoomOut')
		return "zoomOut"
	elif request.args['turnLeft']=='TRUE':
		soilMotors.moveMotor('left')
		return "left"
	elif request.args['Pump1']=='TRUE':
		soilMotors.moveMotor('pump1')
		return "pump1"
	elif request.args['Pump2']=='TRUE':
		soilMotors.moveMotor('pump2')
		return "pump2"
	elif request.args['stop']=='TRUE':
		soilMotors.moveMotor('stop')
		return "stop"
	else:
		return "Unknown Command"

@app.route("/getSensor", methods=['GET', 'POST'])		# Ajax route to send sensor data #! Remove POST Method?
def returnSensorData():
	ph='NoR'
	temp='NoR'
	moisture='NoR'
	pressure='NoR'
	altitute='NoR'
	altitute='NoR'
	uv='NoR'
	if arduinoErr=='None':
		data=arduino.readline()
	# data = '10 20 30 40 50 60'
		data = data.decode('utf-8').rstrip()
		data=data.split(' ')
		ph, temp, moisture, pressure, altitute, uv = data
	return jsonify(
		sensorDataPH=ph, 
		sensorDataTemp=temp, 
		sensorDataMoisture=moisture, 
		sensorDataPressure=pressure,
		sensorDataAltitude=altitute,
		sensorDataUV=uv,
		serialError=arduinoErr,
		)

# Run the app
app.debug=True
app.run('', debug=True,port=8000)

