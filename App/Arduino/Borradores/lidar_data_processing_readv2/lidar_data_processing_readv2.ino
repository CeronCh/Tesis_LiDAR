#include <HardwareSerial.h>
// Parámetros para configuración serial
#define RXD2 16
#define TXD2 17
const int LIDAR_BAUD = 230400;

void setup()
{
  // Se establece la comunicación en serie para visualizar en el monitor serial de la IDE lo que se envía
  Serial.begin(LIDAR_BAUD);
  // Se establece la comunicación en serie entre LiDAR-ESP32
  Serial2.begin(LIDAR_BAUD, SERIAL_8N1, RXD2, TXD2);
}

void loop()
{
  if (Serial2.available())
  {
    byte firstByte = Serial2.read();
    if (firstByte == 0x54) 
    {
      byte secondByte = Serial2.read();
      if (secondByte == 0x2C)
      {
        if (secondByte == 0x2C)
        {
          byte data[47];
          data[0] = firstByte;
          data[1] = secondByte;

          for (int i = 2; i < 47; i++)
          {
            while (!Serial2.available());
            data[i] = Serial2.read();
          }
          String output = "";
          for (int i = 0; i < 47; i++)
          {
            if (data[i] < 0x10) output += "0";
            output += String(data[i], HEX);
          }
          Serial.println(output);
        }                          
      }
    }
  }
}