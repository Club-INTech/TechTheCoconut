/*
 * buffer.h
 *
 *  Created on: 22 déc. 2011
 *      Author: jeremy
 */

#ifndef BUFFER_H_
#define BUFFER_H_

#define BUFFER_SIZE 512

#define PRIM 0xf0
#define SEC 0x0f

#define RIEN 0
#define RFID 1
#define CAM 2
#define LED 3

struct Buffer
{
	char buffer[BUFFER_SIZE];
	unsigned int head;
	unsigned int tail;
} __attribute__((packed));

char bufferRead(unsigned char *octet);

unsigned char bufferAvailable();

char bufferWrite( unsigned char octet);

void traitementLed(unsigned char octet );

void traitement(unsigned char octet);

void pushPwm();
#endif /* BUFFER_H_ */
