#include <SPI.h>
#include <TimerOne.h>
#include <GyverOLED.h>
#include <Wire.h>
#include <EEPROM.h>

#include "BouncePin.h"

// =================================================================================================================================================================================

#define ENCODER_A  2
#define ENCODER_B  3
#define ENCODER_SW 4

#define BTN_CHANGE_PASSWORD 5

#define USE_OLED false

// =================================================================================================================================================================================
// CONSTANTS
// =================================================================================================================================================================================
enum class State: uint8_t {
  Unknown = 0,
  Default,
  Opened,
  PasswordVerification,
  PasswordChanging,
  Timeout
};
const uint32_t PASSWORD_LENGTH = 3;
const uint32_t MAX_PASSWORD_VALUE = 9;
const unsigned long INTERRUPT_INTERVAL = 30; // milliseconds
const unsigned long ENCODER_DEBOUNCE_INTERVAL = 10; // milliseconds
const unsigned long BUTTON_DEBOUNCE_INTERVAL = 50; // milliseconds
const uint32_t MESSAGES_BUFFER_SIZE = 2;
const uint32_t NUM_ATTEMPTS_BEFORE_TIMEOUT = 3;
const unsigned long PASSWORD_TIMEOUT = 5000; // milliseconds

// =================================================================================================================================================================================
// STRUCTS
// =================================================================================================================================================================================

struct PasswordData {
  uint8_t initialized;
  uint32_t password[PASSWORD_LENGTH];
  uint16_t crc;
};

// =================================================================================================================================================================================
// VARIABLES
// =================================================================================================================================================================================
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;

BouncePin pinEncoderA(ENCODER_A, ENCODER_DEBOUNCE_INTERVAL);
BouncePin pinEncoderB(ENCODER_B, ENCODER_DEBOUNCE_INTERVAL);
BouncePin pinEncoderButton(ENCODER_SW, BUTTON_DEBOUNCE_INTERVAL);
BouncePin pinBtnChangePass(BTN_CHANGE_PASSWORD, BUTTON_DEBOUNCE_INTERVAL);

uint32_t password[PASSWORD_LENGTH] = {0, 0, 0};
uint32_t currentPassword[PASSWORD_LENGTH] = {0, 0, 0};
uint32_t currentPassValueIdx = 0;
uint32_t currentAttemptNum = 0;

int lastEncoderState = 0b0000;
bool lastBtnChangePassState = 0;
bool lastEncoderBtnState = 0;

char messagesBuffer[MESSAGES_BUFFER_SIZE][30];
uint32_t currentBufferIdx = 0;
uint32_t numMessages = 0;

unsigned long timeoutStart;

State currentState = State::Default;

bool updateDisplay = false;


// =================================================================================================================================================================================
// HELPER FUNCTIONS
// =================================================================================================================================================================================

void pushMessageToBuffer(const char* message)
{
  for (uint32_t i = 0; i < MESSAGES_BUFFER_SIZE; ++i) {
    if (messagesBuffer[i][0] == '\0') {
      strcpy(messagesBuffer[i], message);
      ++numMessages;
      break;
    }
  }
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void resetCurrentPassword()
{
  currentPassValueIdx = 0;
  for (uint32_t i = 0; i < PASSWORD_LENGTH; ++i) currentPassword[i] = 0;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bool isPasswordCorrect()
{
  for (uint32_t i = 0; i < PASSWORD_LENGTH; ++i) {
    if (currentPassword[i] != password[i]) return false;
  }
  return true;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void changePassword(const uint32_t (&pass)[PASSWORD_LENGTH])
{
  for (uint8_t i = 0; i < PASSWORD_LENGTH; ++i) {
    password[i] = pass[i];
  }

  writePasswordToEEPROM(password);
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void readPasswordFromEEPROM()
{
  PasswordData data;
  EEPROM.get(0, data);

  if (data.initialized == 0xAA) {
    uint16_t crc = 0xAA;
    for(int i = 0; i < PASSWORD_LENGTH; ++i) {
      crc += static_cast<uint8_t>(data.password[i]);
    }
    if (crc == data.crc) {
      for(int i = 0; i < PASSWORD_LENGTH; ++i) {
        password[i] = data.password[i];
      }
    }
  }
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void writePasswordToEEPROM(const uint32_t pass[PASSWORD_LENGTH])
{
  PasswordData data;
  data.initialized = 0xAA;
  
  data.crc = 0xAA;
  for(int i = 0; i < PASSWORD_LENGTH; ++i) {
    data.password[i] = password[i];
    data.crc += static_cast<uint8_t>(password[i]);
  }

  EEPROM.put(0, data);
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void displayMessage(const char* message)
{
  if (USE_OLED) {
    for (size_t i = 0; i < strlen(message); ++i) {
      if (message[i] == ' ') oled.println();
      else oled.print(message[i]);
    }
  } else {
    for (size_t i = 0; i < strlen(message); ++i) {
      Serial.print(message[i]);
    }
    Serial.println();
  }
}


// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// OPEN-CLOSE SAFE FUNCTIONS
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

void openSafe() {}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void closeSafe() {}


// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// UPDATE FUNCTIONS
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void onInterrupt()
{
  if (currentState == State::Timeout) {
    if (millis() - timeoutStart >= PASSWORD_TIMEOUT) {
      currentState = State::Default;
      updateDisplay = true;
    }
    else return;
  }
  
  if (numMessages > 0 || currentState == State::Opened) {
    // update only encoder button
    updateDisplay = updateDisplay | updateEncoderButton();
  } else {
    // update all buttons
    updateDisplay = updateDisplay | updateChangePassButton();
    updateDisplay = updateDisplay | updateEncoderButton();
  }
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bool updateChangePassButton()
{
  bool btnChangePassState = pinBtnChangePass.read();
  if (btnChangePassState != lastBtnChangePassState && btnChangePassState == LOW) {
    handleChangePassButtonRelease();
    lastBtnChangePassState = btnChangePassState;
    return true;
  }

  lastBtnChangePassState = btnChangePassState;
  return false;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void handleChangePassButtonRelease()
{
  if (currentState == State::Default ||
      currentState == State::PasswordChanging ||
      currentState == State::PasswordVerification
  ) {
    currentState = State::PasswordVerification;
    resetCurrentPassword();
    pushMessageToBuffer("Введите текущий пароль");
  }
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bool updateEncoderButton()
{
  bool encoderBtnState = pinEncoderButton.read();
  if (encoderBtnState != lastEncoderBtnState && encoderBtnState == LOW) {
    handleEncoderButtonRelease();
    lastEncoderBtnState = encoderBtnState;
    return true;
  }

  lastEncoderBtnState = encoderBtnState;
  return false;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void handleEncoderButtonRelease()
{
  if (numMessages > 0) {
    if (messagesBuffer[currentBufferIdx][0] == '\0') {
      --numMessages;
      ++currentBufferIdx;
    if (numMessages == 0 || messagesBuffer[currentBufferIdx][0] == '\0') currentBufferIdx = 0;
    }
    return;
  }

  if (currentState == State::Opened) {
    currentState = State::Default;
    pushMessageToBuffer("Сейф закрыт");
    resetCurrentPassword();
    closeSafe();
    updateDisplay = true;
    return;
  }

  // update password value index
  currentPassValueIdx = (currentPassValueIdx < PASSWORD_LENGTH - 1) ? (currentPassValueIdx + 1) : (0);

  if (currentPassValueIdx == 0)
  {
    if (currentState == State::Default) {
      if (isPasswordCorrect()) {
        currentState = State::Opened;
        resetCurrentPassword();
        openSafe();
      } else {
        // handle incorrect password
        if (++currentAttemptNum == NUM_ATTEMPTS_BEFORE_TIMEOUT) {
          timeoutStart = millis();
          currentState = State::Timeout;
          currentAttemptNum = 0;
          updateDisplay = true;
        } else {
          pushMessageToBuffer("Неправильный пароль");
        }
      }
    }
    else if (currentState == State::PasswordVerification) {
      if (isPasswordCorrect()) {
        pushMessageToBuffer("Введите новый пароль");
        currentState = State::PasswordChanging;
      } else {
        pushMessageToBuffer("Введен неверный пароль");
        pushMessageToBuffer("Смена пароля отменена");
        currentState = State::Default;
      }

      resetCurrentPassword();
    }
    else if (currentState == State::PasswordChanging) {
      changePassword(currentPassword);
      resetCurrentPassword();
      pushMessageToBuffer("Пароль успешно изменен");
      currentState = State::Default;
    }
  }
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bool onUpdateEncoder()
{
  if (numMessages > 0) return false;
  if (currentState == State::Opened) return false;
  if (currentState == State::Timeout) return false;

  bool a = pinEncoderA.read();
  bool b = pinEncoderB.read();

  int encoderState = (a << 1) | b;
  int sum = (lastEncoderState << 2) | encoderState;

  if (sum == 0b0010) {
    //                  A  B      A  B      A  B      A  B
    // right rotation: (0, 0) -> (1, 0) -> (1, 1) -> (0, 1)
    handleEncoderLeft();
    updateDisplay = true;
  }
  if (sum == 0b0001) {
    //                 A  B      A  B      A  B      A  B
    // left rotation: (0, 0) -> (0, 1) -> (1, 1) -> (1, 0)
    handleEncoderRight();
    updateDisplay = true;
  }

  lastEncoderState = encoderState;
  updateDisplay = updateDisplay | false;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void handleEncoderLeft()
{
  if (currentPassword[currentPassValueIdx] > 0) --currentPassword[currentPassValueIdx];
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void handleEncoderRight()
{
  if (currentPassword[currentPassValueIdx] < MAX_PASSWORD_VALUE) ++currentPassword[currentPassValueIdx];
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void onUpdateDisplay()
{
  if (USE_OLED) {
    oled.clear();
    oled.home();
  }

  if (numMessages > 0)
  {
    if (USE_OLED) oled.setScale(2);

    // print message and clear it from buffer
    displayMessage(messagesBuffer[currentBufferIdx]);
    
    strcpy(messagesBuffer[currentBufferIdx], "");
  } else {
    if (currentState == State::Opened) {
      if (USE_OLED) oled.setScale(2);
      displayMessage("Сейф открыт");
    } else if (currentState == State::Timeout) {
      if (USE_OLED) oled.setScale(2);
      displayMessage("Превышен лимит попыток. Подожите 5 секунд.");
    } else {
      if (USE_OLED) {
        oled.setScale(4);
        // print current password
        for (uint32_t i = 0; i < PASSWORD_LENGTH; ++i) {
          oled.print(currentPassword[i]);
          oled.print(" ");
          Serial.print(currentPassword[i]);
          Serial.print(" ");
        }
        oled.println();
        
        // print pointer to current password number
        uint32_t i = 0;
        while (i < PASSWORD_LENGTH) {
          if (i++ == currentPassValueIdx) oled.print("|");
          else oled.print("  ");

          if (i++ == currentPassValueIdx) Serial.print("|");
          else Serial.print("  ");
        }
      } else {
        for (uint32_t i = 0; i < PASSWORD_LENGTH; ++i) {
          if (i == currentPassValueIdx) {
            Serial.print("(");
            Serial.print(currentPassword[i]);
            Serial.print(") ");
          } else {
            Serial.print(currentPassword[i]);
            Serial.print(" ");
          }
        }
        Serial.println();
      }
    }
  }
  if (USE_OLED) oled.update();
}


// =================================================================================================================================================================================
// SETUP and LOOP
// =================================================================================================================================================================================
void setup()
{
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  pinMode(ENCODER_SW, INPUT_PULLUP);
  pinMode(BTN_CHANGE_PASSWORD, INPUT_PULLUP);

  if (USE_OLED) {
    oled.init();
    oled.clear();
  }
  Wire.begin();

  readPasswordFromEEPROM();

  // fill buffer with empty strings and push initial message
  for (uint32_t i = 0; i < MESSAGES_BUFFER_SIZE; ++i) strcpy(messagesBuffer[i], "");
  pushMessageToBuffer("Сейф закрыт");

  attachInterrupt(digitalPinToInterrupt(ENCODER_A), onUpdateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_B), onUpdateEncoder, CHANGE);
  Timer1.initialize(1000 * INTERRUPT_INTERVAL);
  Timer1.attachInterrupt(onInterrupt);
  sei();

  if (!USE_OLED) Serial.begin(9600);

  // update display after all initializations
  updateDisplay = true;
}
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void loop()
{
  if (updateDisplay) {
    onUpdateDisplay();
    updateDisplay = false;
  }
}
