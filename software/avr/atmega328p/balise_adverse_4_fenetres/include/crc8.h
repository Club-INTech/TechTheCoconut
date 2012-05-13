#ifndef _CRC8_H_
#define _CRC8_H_

#include <avr/io.h>

#define POLYNOMIAL  0x07

void init_crc8();
void crc8_byte(uint8_t *crc, uint8_t byte);
uint8_t crc8(int32_t data);

#endif
