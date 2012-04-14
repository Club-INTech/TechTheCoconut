#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>
#include "ultrason.h"

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

int main() {
	Serial<0>::init();

	//Pin D2 en INPUT
	cbi(DDRD,PORTD2);
	//Activation des interruptions pour tout changement logique pour pin2
	cbi(EICRA,ISC01);
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite
	
	cbi(DDRD,PORTD3);
	//Activation des interruptions pour tout changement logique pour pin3
	cbi(EICRA,ISC11);
	sbi(EICRA,ISC10);
	sbi(EIMSK,INT1);//Activation proprement dite

	sei();

	while(1) 
	{
		Serial<0>::print(max(ultrason_g.mediane(),ultrason_d.mediane()));
// 		Serial<0>::print(ultrason_d.mediane());
	}
	
	return 0;
}

ISR(TIMER1_OVF_vect){
}


