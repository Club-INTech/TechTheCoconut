#include "timer.h"
#include "utils.h"

template<uint8_t id,uint16_t  PrescalerVal>
Timer::Timer(Prescaler<id,PrescalerVal> prescal) : id_(id)
{
		if(id_==0)
		{
			// Initialisation pin 12
			DDRD |= ( 1 << PORTD6 );
			TCCR0A &= ~( 1 << COM0A0);
			TCCR0A |=  ( 1 << COM0A1 );
			// Fast PWM
			TCCR0A |= ( 1 << WGM00 );
			TCCR0A |= ( 1 << WGM01 );
			TCCR0B &= ~( 1 << WGM02 );
			// Prescaler
			Prescaler<id,PrescalerVal>::set();
		}
		else if(id_==1)
		{
			//Initialisation du comptage
			TIMSK1 |= (1 << TOIE1);
			//Prescaler
			Prescaler<id,PrescalerVal>::set();
		}
		else if(id_==2)
		{
			// Initialisation pin 6
			DDRD |= ( 1 << PORTD3 );
			TCCR2A &= ~( 1 << COM2B0 );
			TCCR2A |= ( 1 << COM2B1 );
			// Fast PWM
			TCCR2A |= ( 1 << WGM20 );
			TCCR2A |= ( 1 << WGM21 );
			TCCR2B &= ~( 1 << WGM22 );
			// Prescaler
			Prescaler<id,PrescalerVal>::set();
		}
}

void Timer::direction(Direction dir)
{
	if(id_==0)
	{
		if(dir == Direction::AVANCER){
		  PORTD &=  ~(1 << PORTD4);
		}
		else if(dir == Direction::RECULER){
		  PORTD |=  (1 << PORTD4);
		}
	}
	else if(id_==2)
	{
		if(dir == Direction::AVANCER){
		  PORTB &=  ~(1 << PORTB0);
		}
		else if(dir == Direction::RECULER){
		  PORTB |=  (1 << PORTB0);
		}
	}
}
	
void Timer::seuil(uint16_t seuil)
{
	if(id_ == 0)
	{
		OCR0A = seuil;
	}
	else if(id_ == 2)
	{
		OCR2B = seuil;
	}
}
