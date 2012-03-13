#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>

//Fonctions de lecture/écriture de bit
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

typedef Timer<1,ModeCounter,8> ClasseTimer;

int main() {

	ClasseTimer::init();
	Serial<0>::init();

	//Pin D2 en INPUT
	cbi(DDRD,PORTD2);
	//Activation des interruptions pour tout changement logique pour pin2
	cbi(EICRA,ISC01);
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite

	sei();

	while(1) 
	{
	}
	
	return 0;
}

ISR(INT0_vect)
{
	//Front montant
	if(rbi(PIND,PORTD2))	{
		ClasseTimer::value(0);
	}else{//Front descendant
		// prescaler/fcpu*inchToCm/tempsParInch
		Serial<0>::print((uint16_t) (ClasseTimer::value()*0.0884353741496));

	}
}

ISR(TIMER1_OVF_vect){
}


