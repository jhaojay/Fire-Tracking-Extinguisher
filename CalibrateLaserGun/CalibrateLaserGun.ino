#include <Servo.h>

Servo upServo;
Servo downServo;

int command = 0;

int switchState = 0;

void setup() {
  Serial.begin(9600);
  
  upServo.attach(11);
  downServo.attach(9);
  pinMode(3, OUTPUT); // laser pin

}

void loop() { 
 
    for(int i = (3310)/2; i < 2700; i = i+0) {
      upServo.writeMicroseconds(964);
      downServo.writeMicroseconds(950);
      delay(1800);
  
      upServo.writeMicroseconds(1614);
      downServo.writeMicroseconds(1600);
      delay(1800);
  
      upServo.writeMicroseconds(2264);
      downServo.writeMicroseconds(2250);
      delay(1800);
    }
  
}
