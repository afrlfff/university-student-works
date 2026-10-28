#define LED_PIN 8

int lState = 70; // F
int latestLedState = 1;


void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  int a = analogRead(A7) / 32;
  Serial.println(a);
  if (!a) a = 1;

  int r = Serial.read();
  if (r == 'T' || r == 'F') lState = r;

  if (lState == 'T') {
    digitalWrite(LED_PIN, latestLedState);
    latestLedState = (latestLedState) ? 0 : 1;
  }
  if (lState == 'F') {
    digitalWrite(LED_PIN, HIGH);
  }

  delay(1000 / a);
}
