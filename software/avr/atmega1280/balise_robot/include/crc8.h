#ifndef _CRC8_H_
#define _CRC8_H_

#include <avr/io.h>

#ifndef _FRAME_TYPEDEF_
#define _FRAME_TYPEDEF_
typedef int32_t Data;
typedef uint8_t Crc;
#endif


#define POLYNOMIAL  0x07

void init_crc8();
void crc8_byte(Crc *crc, uint8_t byte);
Crc crc8(Data data);

#endif
