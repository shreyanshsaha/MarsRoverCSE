#include <Stepper.h>
//separate functions for all controls
//Pins for stepper
const int stepsPerRevolution = 200;
String val;
//black-out4
//red-out3
//orange-out1
//green-out2

// Pumps
// gate of mosfets to pins 7 and 8

// zoom
// in1-9 in2-10

//arduino common ground w/  all 3 sources

Stepper myStepper(stepsPerRevolution, 3, 4, 5, 6);

//pumps
int m1 = 7;
int m2 = 8;

//zoom
int in1 = 9;
int in2 = 10;

void pump1() //activates pump
{
	Serial.println("Pump 1");
	digitalWrite(m1, HIGH);
	digitalWrite(m2, LOW);
}

void pump2()
{
	Serial.println("Pump 2");
	digitalWrite(m2, HIGH);
	digitalWrite(m1, LOW);
}

void stopp() // stops all pumps
{
	Serial.println("Stop");
	digitalWrite(m1, LOW);
	digitalWrite(m2, LOW);
}

//stepper
void stepma() //anti
{
	Serial.println("Step Anti Clockwise");
	myStepper.step(700 / 6); //one sixth rev
	val = "0";
}
void stepmc() //clockwise
{
	Serial.println("Step Clockwise");
	myStepper.step(-700 / 6);
	val = "0";
}

//microscope zoom
void zoomi() //zoom in
{
	Serial.println("Zoom In");
	digitalWrite(in1, HIGH);
	digitalWrite(in2, LOW);
	delay(350);
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	val = "0";
}

void zoomo() //zoom out
{
	Serial.println("Zoom Out");
	digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	delay(350);
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	val = "0";
}

void setup()
{

	myStepper.setSpeed(30);

	pinMode(m1, OUTPUT);
	pinMode(m2, OUTPUT);
	digitalWrite(m1, LOW);
	digitalWrite(m2, LOW);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	digitalWrite(in2, LOW);
	digitalWrite(in1, LOW);
	Serial.begin(9600);
	val = "0";

	Serial.println("Initialized");
}
void loop()
{
	if (Serial.available())
	{
		val = Serial.readString();
		if (val == "a") //stepper control anti c
		{
			stepma();
		}
		else if (val == "c") // clockwise
		{
			stepmc();
		}
		else if (val == "1")
		{
			pump1(); //activate pump 1
		}

		else if (val == "2")
		{
			pump2(); //activate pump 1
		}
		else if (val == "s")
		{
			stopp(); // stop both
		}

		else if (val == "i")
		{
			zoomi(); //in
		}

		else if (val == "o")
		{
			zoomo(); //out
		}
	}
}
