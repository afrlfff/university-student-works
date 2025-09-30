const int N = 11;
const int LED_PINS[N] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
const unsigned long lightDuration = 250;

void forward()
{
  digitalWrite(LED_PINS[0], HIGH); // turn on first
  delay(lightDuration);

  for (int i = 1; i < N; ++i) {
    digitalWrite(LED_PINS[i], HIGH); // turn on current
    digitalWrite(LED_PINS[i - 1], LOW); // turn off previous
    delay(lightDuration);
  }

  digitalWrite(LED_PINS[N - 1], LOW); // turn off last
}

void backward()
{
  digitalWrite(LED_PINS[N - 1], HIGH); // turn on first
  delay(lightDuration);

  for (int i = 1; i < N; ++i) {
    digitalWrite(LED_PINS[N - i - 1], HIGH); // turn on current
    digitalWrite(LED_PINS[N - i], LOW); // turn off previous
    delay(lightDuration);
  }

  digitalWrite(LED_PINS[0], LOW); // turn off last
}

void setup()
{
  for (int i = 0; i < N; ++i) {
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop()
{
  forward();
  delay(lightDuration);
  backward();
  delay(lightDuration);
}












