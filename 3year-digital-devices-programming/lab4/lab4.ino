#include <TimerOne.h>

#define KEY1 2
#define KEY2 12
#define BUZZER 5

uint8_t btnOneState = 0;
uint8_t btnTwoState = 1;
uint8_t btnPressed = 0;
const uint8_t leds[] = {4, 8, 9};
int8_t curLed = 0;
bool inputBlocked = false;
uint8_t interruptsSkipped = 0;

void handleButton() {
  if (btnPressed == 1) {
    if (curLed - 1 < 0) {
      digitalWrite(BUZZER, HIGH);
      curLed = 0;
      return;
    }
    digitalWrite(leds[curLed - 1], LOW);
    curLed--;
  }
  else {
    if (curLed - 1 == 3) {
      digitalWrite(BUZZER, HIGH);
      curLed = 3;
      return;
    }
    curLed++;
    digitalWrite(leds[curLed - 1], HIGH);
  }
}

void onInterrupt() {
  if (!inputBlocked) {
    uint8_t curKey1 = digitalRead(KEY1);
    uint8_t curKey2 = digitalRead(KEY2);
    if (btnOneState != curKey1) {
      inputBlocked = true;
      btnPressed = 1;
      btnOneState = curKey1;
      handleButton();
    }
    if (btnTwoState != curKey2 && !inputBlocked) {
      inputBlocked = true;
      btnPressed = 2;
      btnTwoState = curKey2;
      handleButton();
    }
    Serial.println(curLed);
  }
  else {
    if (interruptsSkipped == 2) {
      interruptsSkipped = 0;
      inputBlocked = false;
      digitalWrite(BUZZER, LOW);
      if (btnPressed == 1) {
        btnOneState = !btnOneState;
      }
      else {
        btnTwoState = !btnTwoState;
      }
    }
    else {
      interruptsSkipped++;
    }
  }
}

void setup() {
  Serial.begin(9600);
  Timer1.initialize(1000 * 30);
  Timer1.attachInterrupt(onInterrupt);
  sei();
  pinMode(KEY1, INPUT);
  pinMode(KEY2, INPUT);
  pinMode(leds[0], OUTPUT);
  pinMode(leds[1], OUTPUT);
  pinMode(leds[2], OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);
  digitalWrite(leds[0], LOW);
  digitalWrite(leds[1], LOW);
  digitalWrite(leds[2], LOW);
}

void loop() { }
