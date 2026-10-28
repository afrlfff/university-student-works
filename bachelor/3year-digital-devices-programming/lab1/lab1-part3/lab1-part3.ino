#include <TimerOne.h>

const int N = 11;
const int LED_PINS[N] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
const unsigned long lightDuration = 250; // 1 second

int stepCounter = 0;
bool forward = true;


void garland()
{
  if (forward) {
    forward_step(stepCounter++);
  } else {
    backward_step(stepCounter++);
  }

  if (stepCounter > N) {
    // reverse direction
    forward = !forward;
    stepCounter = 0;
  }
}

void forward_step(const int stepIndex)
{
  if (stepIndex == 0) {
    digitalWrite(LED_PINS[0], HIGH); // turn on first
  } else if (stepIndex == N) {
    digitalWrite(LED_PINS[N - 1], LOW); // turn off last
  } else {
    digitalWrite(LED_PINS[stepIndex], HIGH); // turn on current
    digitalWrite(LED_PINS[stepIndex - 1], LOW); // turn off previous
  }
}

void backward_step(const int stepIndex)
{
  if (stepIndex == 0) {
    digitalWrite(LED_PINS[N - 1], HIGH); // turn on first
  } else if (stepIndex == N) {
    digitalWrite(LED_PINS[0], LOW); // turn off last
  } else {
    digitalWrite(LED_PINS[N - stepIndex - 1], HIGH); // turn on current
    digitalWrite(LED_PINS[N - stepIndex], LOW); // turn off previous
  }
}

void setup()
{
  Timer1.initialize(lightDuration * 1000);
  Timer1.attachInterrupt(garland);
  sei(); // allow interrupts

  for (int i = 0; i < N; ++i) {
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop() { }












