
#include <HardwareSerial.h>
// Parámetros para configuración serial
#define RXD2 16
#define TXD2 17
// Elección de Switch Case
#define FULL_DATA 0
#define RELEVANT_DATA 1
#define RELEVANT_DATA2 2
// Parámetros constantes
const int LIDAR_BAUD = 230400;
// Constantes para la longitud de los diferentes campos del paquete
const int packet_length = 47;                   // Longitud total del paquete por medicion
const int key_data_length = 30;                 // Longitud del paquete con datos de medición relevantes
const int key_data2_length = 42;                 // Longitud del paquete con datos de medición relevantes
const int packet_length_bits = 95;              // Longitud total del paquete por medicion en bits + /n
char data_sent[packet_length_bits];
char* data_sent_ptr;
// Tabla de verificación de CRC proporcionada por los desarrolladores
static const uint8_t CrcTable[256]=
{ 
  0x00, 0x4d, 0x9a, 0xd7, 0x79, 0x34, 0xe3, 0xae,
  0xf2, 0xbf, 0x68, 0x25, 0x8b, 0xc6, 0x11, 0x5c,
  0xa9, 0xe4, 0x33, 0x7e, 0xd0, 0x9d, 0x4a, 0x07,
  0x5b, 0x16, 0xc1, 0x8c, 0x22, 0x6f, 0xb8, 0xf5,
  0x1f, 0x52, 0x85, 0xc8, 0x66, 0x2b, 0xfc, 0xb1,
  0xed, 0xa0, 0x77, 0x3a, 0x94, 0xd9, 0x0e, 0x43,
  0xb6, 0xfb, 0x2c, 0x61, 0xcf, 0x82, 0x55, 0x18,
  0x44, 0x09, 0xde, 0x93, 0x3d, 0x70, 0xa7, 0xea,
  0x3e, 0x73, 0xa4, 0xe9, 0x47, 0x0a, 0xdd, 0x90,
  0xcc, 0x81, 0x56, 0x1b, 0xb5, 0xf8, 0x2f, 0x62,
  0x97, 0xda, 0x0d, 0x40, 0xee, 0xa3, 0x74, 0x39,
  0x65, 0x28, 0xff, 0xb2, 0x1c, 0x51, 0x86, 0xcb,
  0x21, 0x6c, 0xbb, 0xf6, 0x58, 0x15, 0xc2, 0x8f,
  0xd3, 0x9e, 0x49, 0x04, 0xaa, 0xe7, 0x30, 0x7d,
  0x88, 0xc5, 0x12, 0x5f, 0xf1, 0xbc, 0x6b, 0x26,
  0x7a, 0x37, 0xe0, 0xad, 0x03, 0x4e, 0x99, 0xd4,
  0x7c, 0x31, 0xe6, 0xab, 0x05, 0x48, 0x9f, 0xd2,
  0x8e, 0xc3, 0x14, 0x59, 0xf7, 0xba, 0x6d, 0x20,
  0xd5, 0x98, 0x4f, 0x02, 0xac, 0xe1, 0x36, 0x7b,
  0x27, 0x6a, 0xbd, 0xf0, 0x5e, 0x13, 0xc4, 0x89,
  0x63, 0x2e, 0xf9, 0xb4, 0x1a, 0x57, 0x80, 0xcd,
  0x91, 0xdc, 0x0b, 0x46, 0xe8, 0xa5, 0x72, 0x3f,
  0xca, 0x87, 0x50, 0x1d, 0xb3, 0xfe, 0x29, 0x64,
  0x38, 0x75, 0xa2, 0xef, 0x41, 0x0c, 0xdb, 0x96,
  0x42, 0x0f, 0xd8, 0x95, 0x3b, 0x76, 0xa1, 0xec,
  0xb0, 0xfd, 0x2a, 0x67, 0xc9, 0x84, 0x53, 0x1e,
  0xeb, 0xa6, 0x71, 0x3c, 0x92, 0xdf, 0x08, 0x45,
  0x19, 0x54, 0x83, 0xce, 0x60, 0x2d, 0xfa, 0xb7,
  0x5d, 0x10, 0xc7, 0x8a, 0x24, 0x69, 0xbe, 0xf3,
  0xaf, 0xe2, 0x35, 0x78, 0xd6, 0x9b, 0x4c, 0x01,
  0xf4, 0xb9, 0x6e, 0x23, 0x8d, 0xc0, 0x17, 0x5a,
  0x06, 0x4b, 0x9c, 0xd1, 0x7f, 0x32, 0xe5, 0xa8
};


uint8_t CalCRC8(uint8_t *data_in, uint8_t len)
{
  uint8_t crc = 0;                            // Se inicializa la variable crc en 0
  for (uint16_t i = 0; i < len; i++)          // Se recorre cada byte del array de datos apuntados 
  {
    crc = CrcTable[(crc ^ *data_in++) & 0xff];// XOR entre crc y el valor del puntero que se incrementa en cada ciclo
  }
  return crc;
}

byte* read_lidar(int data_type)
{
  static byte data[packet_length];
  static byte key_data[key_data_length];
  static byte key_data2[key_data2_length];
  if (Serial2.available())
  {
    byte first_header = Serial2.read();
    if (first_header == 0x54) 
    {
      byte second_header = Serial2.read();
      if (second_header == 0x2C)
      {
        data[0] = first_header;
        data[1] = second_header;
        for (int i = 2; i < 47; i++)
        {
          while (!Serial2.available());
          data[i] = Serial2.read();
        }
        uint8_t crc_calc = CalCRC8(data, packet_length-1);
        uint8_t crc_rec = data[46];
        if(crc_calc == crc_rec)
        {
          if(data_type == FULL_DATA)
          {
            return data;
          }
          else if (data_type == RELEVANT_DATA)
          {
            key_data[0] = data[0];
            key_data[1] = data[1];
            key_data[2] = data[4];
            key_data[3] = data[5];
            for (int i = 0; i < 12; i++)
            {
              key_data[4 + i * 2] = data[6 + i * 3];
              key_data[5 + i * 2] = data[7 + i * 3];
            }
            key_data[28] = data[42];
            key_data[29] = data[43];

            return key_data;
          }
          else if (data_type == RELEVANT_DATA2)
          {
            key_data2[0] = data[0];
            key_data2[1] = data[1];
            key_data2[2] = data[4];
            key_data2[3] = data[5];
            for (int i = 0; i < 12; i++)
            {
              key_data2[4 + i * 3] = data[6 + i * 3];
              key_data2[5 + i * 3] = data[7 + i * 3];
              key_data2[6 + i * 3] = data[8 + i * 3];
            }
            key_data2[40] = data[42];
            key_data2[41] = data[43];

            return key_data2;
          }
        }             
      }
    }
  }
  return nullptr;
}

void send_data(byte* data, int data_type)
{
  if(data != nullptr)
  {
    data_sent_ptr = data_sent;
    if(data_type == FULL_DATA)
    {
      for (int i = 0; i < 47; i++)
      {
        data_sent_ptr += sprintf(data_sent_ptr, "%02X", data[i]);
      }
    }
    else if (data_type == RELEVANT_DATA)
    {
      for (int i = 0; i < 30; i++)
      {
        data_sent_ptr += sprintf(data_sent_ptr, "%02X", data[i]);
      }
    }
    else if (data_type == RELEVANT_DATA2)
    {
      for (int i = 0; i < 42; i++)
      {
        data_sent_ptr += sprintf(data_sent_ptr, "%02X", data[i]);
      }
    }
    Serial.println(data_sent);
  }
}

void setup()
{
  // Se establece la comunicación en serie para visualizar en el monitor serial de la IDE lo que se envía
  Serial.begin(LIDAR_BAUD);
  // Se establece la comunicación en serie entre LiDAR-ESP32
  Serial2.begin(LIDAR_BAUD, SERIAL_8N1, RXD2, TXD2);
}

void loop()
{
  int data_type = RELEVANT_DATA;
  byte* lidar_data = read_lidar(data_type);
  send_data(lidar_data, data_type);
}