#include <SoftwareSerial.h>

int pwm0 = 4;
int dir0 = 5;

int pwm1 = 6;
int dir1 = 7;

int pwm2 = 8;
int dir2 = 9;

int pwm3 = A0;
int dir3 = 10;

int pwm4 = A3;
int dir4 = 11;

int pwm5 = A4;
int dir5 = 12;

Cytron_PS2Shield ps2(10, 11);

void moveMotor(String inp) {
  if (inp == "0") {
    digitalWrite(pwm0, HIGH);
    digitalWrite(dir0, HIGH);

  } else if (inp == "1") {
    digitalWrite(pwm0, HIGH);
    digitalWrite(dir0, LOW);
  } else if (inp == "2") {
    digitalWrite(pwm1, HIGH);
    digitalWrite(dir1, HIGH);
  } else if (inp == "3") {
    digitalWrite(pwm1, HIGH);
    digitalWrite(dir1, LOW);

  }

  else if (inp == "4") {
    digitalWrite(pwm2, HIGH);
    digitalWrite(dir2, HIGH);
  } else if (inp == "5") {
    digitalWrite(pwm2, HIGH);
    digitalWrite(dir2, LOW);
  } else if (inp == "6") {
    digitalWrite(pwm3, HIGH);
    digitalWrite(dir3, HIGH);
  } else if (inp == "7") {
    digitalWrite(pwm3, HIGH);
    digitalWrite(dir3, LOW);
  } else if (inp == "c") {
    digitalWrite(pwm4, HIGH);
    digitalWrite(dir4, HIGH);
  } else if (inp == "t") {
    digitalWrite(pwm5, HIGH);
    digitalWrite(dir5, HIGH);
  } else if (inp == "x") {
    digitalWrite(pwm5, HIGH);
    digitalWrite(dir5, LOW);
  } else if (inp == "s") {
    digitalWrite(pwm4, HIGH);
    digitalWrite(dir4, LOW);
  } else if (inp == "a") {
    digitalWrite(pwm0, LOW);

    digitalWrite(pwm1, LOW);

    digitalWrite(pwm2, LOW);

    digitalWrite(pwm3, LOW);

    digitalWrite(pwm4, LOW);

    digitalWrite(pwm5, LOW);
  }
}

void setup() {
  ps2.begin(9600);
  Serial.begin(9600);

  Serial.println("Initialized");
  pinMode(pwm0, OUTPUT);
  pinMode(dir0, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm3, OUTPUT);
  pinMode(dir3, OUTPUT);
  pinMode(pwm4, OUTPUT);
  pinMode(dir4, OUTPUT);
  pinMode(pwm5, OUTPUT);
  pinMode(dir5, OUTPUT);
}

void loop() {
  Select = ps2.readButton(PS2_SELECT);
  Start = ps2.readButton(PS2_START);
  Ps2_UP = ps2.readButton(PS2_UP);
  Ps2_DOWN = ps2.readButton(PS2_DOWN);
  Ps2_RIGHT = ps2.readButton(PS2_RIGHT);
  Ps2_LEFT = ps2.readButton(PS2_LEFT);
  Ps2_LEFT1 = ps2.readButton(PS2_LEFT_1);
  Ps2_LEFT2 = ps2.readButton(PS2_LEFT_2);
  Ps2_RIGHT1 = ps2.readButton(PS2_RIGHT_1);
  Ps2_RIGHT2 = ps2.readButton(PS2_RIGHT_2);
  Ps2_TRIANGLE = ps2.readButton(PS2_TRIANGLE);
  Ps2_CIRCLE = ps2.readButton(PS2_CIRCLE);
  Ps2_CROSS = ps2.readButton(PS2_CROSS);
  Ps2_SQUARE = ps2.readButton(PS2_SQUARE);

  if (Ps2_LEFT == 0) {
    current = '0';
  } else if (Ps2_RIGHT == 0) {
    current = '1';
  } else if (Ps2_UP == 0) {
    current = '2';
  } else if (Ps2_DOWN == 0) {
    current = '3';
  } else if (Ps2_LEFT1 == 0) {
    current = '4';
  } else if (Ps2_LEFT2 == 0) {
    current = '5';
  } else if (Ps2_RIGHT1 == 0) {
    current = '6';
  } else if (Ps2_RIGHT2 == 0) {
    current = '7';
  } else if (Ps2_CIRCLE == 0) {
    current = 'c';
  } else if (Ps2_TRIANGLE == 0) {
    current = 't';
  } else if (Ps2_CROSS == 0) {
    current = 'x';
  } else if (Ps2_SQUARE == 0) {
    current = 's';
  } else {
    current = 'a';
  }
  moveMotor(current);
  Serial.println(current);
}
