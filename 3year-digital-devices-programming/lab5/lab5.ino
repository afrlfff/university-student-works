#include <GyverOLED.h>
#include <microDS18B20.h>
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>


MicroDS18B20<10> sensor;
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;
MPU6050 mpu;
float curTemp = 0;


void setup() {
  Serial.begin(9600);
  oled.init();
  oled.clear();
  oled.setScale(3);
  Wire.begin();
  mpu.initialize();
  Serial.println(mpu.testConnection());
}

void loop() {
  sensor.requestTemp();
  float value = 0.f;
  int16_t ax = mpu.getAccelerationX();
  int16_t ay = mpu.getAccelerationY();
  int16_t az = mpu.getAccelerationZ();
  if (sensor.readTemp()) value = sensor.getTemp();
  if (curTemp != value) {
    oled.home();
    oled.setScale(3);
    oled.print("T:");
    oled.println(value);
    curTemp = value;
    oled.setScale(1);
    oled.print("X:");
    oled.println(ax);
    oled.print("Y:");
    oled.println(ay);
    oled.print("Z:");
    oled.print(az);
  }
  delay(100);
}
