// this code can be found in arduino ide examples: StandardFirmata

#include <Servo.h>
#include <Wire.h>
#include <Firmata.h>

void setup() {
  Firmata.begin(57600);
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput(); // waits and decodes commands from PC
  }
}
