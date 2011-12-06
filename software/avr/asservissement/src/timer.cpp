#include "timer.h"


Timer::Timer(TimerId id, Prescaler ratio) : id_(id)
{
		if(id_==TimerId::T0)
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
			TCCR0B |= ratio.underlying();
		}
		else if(id_==TimerId::T1)
		{
			//Initialisation du comptage
			TIMSK1 |= (1 << TOIE1);
			//Prescaler
			TCCR1B |= ratio.underlying();
		}
		else if(id_==TimerId::T2)
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
			TCCR2B |= ratio.underlying();
		}
}

void Timer::direction(Direction dir)
{
	if(id_==TimerId::T0)
	{
		if(dir == Direction::AVANCER){
		  PORTD &=  ~(1 << PORTD4);
		}
		else if(dir == Direction::RECULER){
		  PORTD |=  (1 << PORTD4);
		}
	}
	else if(id_==TimerId::T2)
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
	if(id_ == TimerId::T0)
	{
		OCR0A = seuil;
	}
	else if(id_ == TimerId::T2)
	{
		OCR2B = seuil;
	}
}
