#include "BluetoothSerial.h"
#include <HardwareSerial.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
HardwareSerial SerialPort(2); // use UART2
String data = "";

void setup() {
  Serial.begin(9600);
  SerialPort.begin(9600, SERIAL_8N1, 16, 17); 
  SerialBT.begin("ESP32BT"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
}

void loop() {
  // if (Serial.available()) {
  //   data = Serial.readString();
  //   SerialBT.print(data);
  //   SerialPort.write(data.c_str());
  // }
  if (SerialBT.available()) {
    data = "[esp]"+SerialBT.readString();
    Serial.write(data.c_str());
    SerialPort.write(data.c_str());
  }
  if (SerialPort.available()) {
    data = "[STM]"+SerialPort.readString();
    Serial.write(data.c_str());
    SerialBT.print(data);
  }
  
  delay(20);
}
