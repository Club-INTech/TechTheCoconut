#ifdef __cplusplus
extern "C" {
#endif

#ifndef ADC_H
#define ADC_H

#include <avr/io.h>
#include <avr/interrupt.h>

#define ADC_BUFFER_SIZE 16

/**
 * Permet de rajouter le mode interruption à la lib
 */
//#define __ADC_INTERRUPT__

/**
 * Ces defines permettent de choisir quel ADC nous voulons utiliser
 * Ne pas mettre autre chose dans les types que les defines ci-dessous
 */
#define ADC0 0
#define ADC1 1
#define ADC2 2
#define ADC3 3
#define ADC4 4
#define ADC5 5
#define ADC6 6
#define ADC7 7
#define ADC8 8
#define ADC11 14
#define ADCGND 15

/**
 * Ces defines permettent de choisir quel est la tension de référence
 * 00 ==> AREF
 * 01 ==> AVcc
 * 11 ==> Interne à 1.1V
 */
#define ADC_REF0 4
#define ADC_REF1 5

/**
 * Permet de choisir entre le mode interruption ou pull
 * 1 ==> PULL
 * 0 ==> Interruption
 */
#define ADC_CHOOSE 6

/**
 * Valeur de conf à utiliser de préférence par rapport à la valeur elle-même (c'est plus clair)
 */
#define ADC_INTERRUPT 0
#define ADC_PULL 1


struct adcValeur
{
	uint16_t buffer;
	unsigned char type;
};

struct adcRingBuffer
{
	struct adcValeur buffer[ADC_BUFFER_SIZE];
	unsigned char head;
	unsigned char tail;
};

void adcInit( unsigned char);

void adcAjoutPin( unsigned char);

void adcClose();

#ifdef __ADC_INTERRUPT__
unsigned char adcAvailable();
#endif

int adcRead(unsigned char );

/**
 * Attention, si le type vaut 0xf0, c'est que le buffer était vide
 */
#ifdef __ADC_INTERRUPT__
struct adcValeur adcReadBuffer();
#endif



#endif

#ifdef __cplusplus
}
#endif
