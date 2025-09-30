const int LED_PIN = 8;
const int BTN_PIN = 2;

int ledState = HIGH; // по умолчанию светодиод не горит
int btnState = LOW; // по умолчанию кнопка не нажата
int btnStatePrev;
unsigned long previousMillis = 0;
unsigned long interval = 1000; // интервал для задания 1 секунда


void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT);

  digitalWrite(LED_PIN, ledState);

  // pinMode(BIN_PIN, INPUT_PULLUP);
}

void loop()
{
  btnStatePrev = btnState;
  btnState = digitalRead(BTN_PIN);
  unsigned long currentMillis = millis();

  delay(50);

  if (btnState == HIGH && btnStatePrev == LOW)
  {
    // if button was pressed
    previousMillis = currentMillis;
  }
  if (btnState == LOW && btnStatePrev == HIGH)
  {
    // if button was released
    // change LED state if lower that {interval} milliseconds passed
    if (currentMillis - previousMillis < interval) {
      ledState = (ledState == LOW) ? HIGH : LOW;
    }
    // update LED state
    digitalWrite(LED_PIN, ledState);
  }
}
















/* const int LED_PIN = 8;
const int BTN_PIN = 2;

int ledState = HIGH; // по умолчанию светодиод не горит
int btnState = LOW; // по умолчанию кнопка не нажата
int btnStatePrev;
unsigned long previousMillis = 0;
unsigned long interval = 1000; // интервал для задания 1 секунда


void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT);

  // pinMode(BIN_PIN, INPUT_PULLUP);
}

void loop()
{
  btnStatePrev = btnState;
  btnState = digitalRead(BTN_PIN);
  unsigned long currentMillis = millis();

  Serial.println(btnState);
  delay(50);

  if (btnState == HIGH && btnStatePrev == LOW)
  {
    // if button was pressed
    previousMillis = currentMillis;
  }
  if (btnState == LOW && btnStatePrev == HIGH)
  {
    // if button was released
    // change LED state if lower that {interval} milliseconds passed
    if (currentMillis - previousMillis < interval) {
      ledState = (ledState == LOW) ? HIGH : LOW;
    }
    // update LED state
    digitalWrite(LED_PIN, ledState);
  }
  
} */