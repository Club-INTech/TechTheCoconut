/*
 * buffer.c
 *
 *  Created on: 22 déc. 2011
 *      Author: jeremy
 */

#include "buffer.h"
#include "pwm.h"

struct Buffer buffer = {{0},0,0};

unsigned char etat = 0;
unsigned int pwm = 0;

char bufferRead(unsigned char *octet)
{
	if( buffer.head == buffer.tail)
		return -1;
	else
	{
		*octet = buffer.buffer[buffer.tail];
		buffer.tail = (buffer.tail + 1 ) % BUFFER_SIZE;
	}
	return 0;
}

unsigned char bufferAvailable()
{
	return (( BUFFER_SIZE + buffer.head - buffer.tail) % BUFFER_SIZE );
}

char bufferWrite( unsigned char octet)
{
	unsigned int i = (buffer.head + 1) % BUFFER_SIZE;
	if( i != buffer.tail)
	{
		buffer.buffer[buffer.head] = octet;
		buffer.head = i;
		return 0;
	}
	else
		return -1;
}

void traitement(unsigned char octet)
{
	switch( etat & PRIM)
	{
	case RIEN :
		switch( octet )
		{
		case 'l' :
			etat |= ( LED << 4 );
			break;
		case 'r' :
			etat |= ( RFID << 4 );
			break;
		case 'c' :
			etat |= ( CAM << 4 );
			break;
		default:
			break;
		}
		break;
	case LED :
		if( octet < '9' & octet > '0')
			traitementLed( octet);
		switch( octet )
		{
		case '\n' :
			etat = 0x00;
			pushPwm();
			break;
		case 'g' :
			break;
		case 'b' :
			break;
		case 'r' :
			break;
		default :
			etat = 0x00;
			break;
		}
		break;
	case RFID :
		break;
	case CAM :
		break;
	default :
		break;
	}
}

void traitementLed(unsigned char octet )
{
	switch( octet )
	{
		case '0' :
			pwm *= 10;
			break;
		case '1' :
			pwm *= 10;
			pwm += 1;
			break;
		case '2' :
			pwm *= 10;
			pwm += 2;
			break;
		case '3' :
			pwm *= 10;
			pwm += 3;
			break;
		case '4' :
			pwm *= 10;
			pwm += 5;
			break;
		case '5' :
			pwm *= 10;
			pwm += 6;
			break;
		case '6' :
			pwm *= 10;
			pwm += 6;
			break;
		case '7' :
			pwm *= 10;
			pwm += 7;
			break;
		case '8' :
			pwm *= 10;
			pwm += 8;
			break;
		case '9' :
			pwm *= 10;
			pwm += 9;
			break;
		default :
			break;
	}
}

void pushPwm()
{
	int puissance = (int)pwm - 600;
	switch( etat & SEC )
	{
	case ROUGE :
		PWM_Update(ROUGE,puissance);
		break;
	case VERT :
		PWM_Update(VERT,puissance);
		break;
	case BLEU :
		PWM_Update(BLEU,puissance);
		break;
	}
}
