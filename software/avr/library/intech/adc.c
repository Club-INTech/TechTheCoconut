#include "adc.h"

#ifdef __ADC_INTERRUPT__
struct adcRingBuffer adcBuffer = { { { 0 , 0 } }, 0, 0 };

ISR(ADC_vect)
{
	int i = (adcBuffer.head + 1) % ADC_BUFFER_SIZE;
	if (i != adcBuffer.tail)
	{
		adcBuffer.buffer[adcBuffer.head].buffer = (ADCH << 8) | ADCL ;
		adcBuffer.buffer[adcBuffer.head].type = ADMUX & 0x0f;
		adcBuffer.head = i;
	}
}

unsigned char adcAvailable()
{
	return (ADC_BUFFER_SIZE + adcBuffer.head - adcBuffer.tail) % ADC_BUFFER_SIZE;
}
#endif

void adcInit(unsigned char conf)
{
	//Activation du système de convertion
	ADCSRA |= ( 1 << ADEN );

	//Choix de la clock : division par 128
	ADCSRA |= ( 1 << ADPS2 ) | ( 1 << ADPS1 ) | ( 1 << ADPS0 );

	//Configuration du port
	adcAjoutPin(conf & 0x0f);

	//Choix de la tension de référence
	switch( (conf & ( ( 1 << ADC_REF0 ) | ( 1 << ADC_REF1 ) ) ) >> ADC_REF0 )
	{
		case 0:
			ADMUX &= ~( ( 1 << REFS1 ) | ( 1 << REFS0 ));
			break;
		case 1:
			ADMUX &= ~( 1 << REFS1 );
			ADMUX |= ( 1 << REFS0 );
			break;
		case 3:
			ADMUX |= ( ( 1 << REFS1 ) | ( 1 << REFS0 ) );
			break;
		default:
			break;
	}

	//Choix de l'adc à lire
	ADMUX |= conf & 0x0f;
	ADMUX &= ~( ~( conf & 0x0f ) & 0x0f );

	// Intérruption ?
	ADCSRA &= ~( 1 << ADIE );
#ifdef __ADC_INTERRUPT__
	if( (conf & ( 1 << ADC_CHOOSE)) == ADC_INTERRUPT )
	{
		//Mise en mode continue
		ADCSRB &= ~( ( 1 << ADTS2 ) | ( 1 << ADTS1 ) | ( 1 << ADTS0 ) );
		//Activation des interruptions
		ADCSRA |= ( 1 << ADIE );
		//Activation de la convertion
		ADCSRA |= ( 1 << ADSC);
	}
#endif
}

void adcClose()
{
	//Désactivation du système d'interruption
	ADCSRA &= ( 1 << ADEN );
}

void adcAjoutPin(unsigned char pin)
{
	switch( pin & 0x0f)
	{
		case ADC0:
			DDRC &= ~( 1 << PORTC0 );
			PORTC &= ~( 1 << PORTC0 );
			break;
		case ADC1:
			DDRC &= ~( 1 << PORTC1 );
			PORTC &= ~( 1 << PORTC1 );
			break;
		case ADC2:
			DDRC &= ~( 1 << PORTC2 );
			PORTC &= ~( 1 << PORTC2 );
			break;
		case ADC3:
			DDRC &= ~( 1 << PORTC3 );
			PORTC &= ~( 1 << PORTC3 );
			break;
		case ADC4:
			DDRC &= ~( 1 << PORTC4 );
			PORTC &= ~( 1 << PORTC4 );
			break;
		case ADC5:
			DDRC &= ~( 1 << PORTC5 );
			PORTC &= ~( 1 << PORTC5 );
			break;
		default:
			break;
	}
}

int adcRead(unsigned char type)
{
	adcAjoutPin(type);
	ADMUX |= type;
	ADCSRA |= ( 1 << ADSC );
	while( ADCSRA & ( 1 << ADSC ));
	uint8_t low = ADCL, high = ADCH;
	return (high << 8) | low ;
}

#ifdef __ADC_INTERRUPT__
struct adcValeur adcReadBuffer()
{
	struct adcValeur valeur= { 0, 0xf0 };
	if (adcBuffer.head != adcBuffer.tail)
	{
		valeur.buffer = adcBuffer.buffer[adcBuffer.tail].buffer;
		valeur.type = adcBuffer.buffer[adcBuffer.tail].type;
		adcBuffer.tail = (adcBuffer.tail + 1) % ADC_BUFFER_SIZE;
	}
	return valeur;
}
#endif