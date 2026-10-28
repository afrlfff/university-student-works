const unsigned long signalDelay = 250;
const unsigned long letterDelay = 1000;
const unsigned long dotDuration = 250;
const unsigned long dashDuration = 500;
const int LED_PIN = 8;


void dot()
{
  digitalWrite(LED_PIN, LOW);
  delay(dotDuration);
  digitalWrite(LED_PIN, HIGH);
}

void dash()
{
  digitalWrite(LED_PIN, LOW);
  delay(dashDuration);
  digitalWrite(LED_PIN, HIGH);
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop()
{
  // L
  dot();
  delay(signalDelay);
  dash();
  delay(signalDelay);
  dot();
  delay(signalDelay);
  dot();
  delay(letterDelay);

  // E
  dot();
  delay(letterDelay);

  // T
  dash();
  delay(letterDelay);

  // I
  dot();
  delay(signalDelay);
  dot();
  delay(signalDelay);
  delay(letterDelay);
}












