#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/timer.hpp>

#include <stdint.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "balise.h"
#include "frame.h"
#include "crc8.h"
#include "utils.h"

//Fonctions de modifications de bits
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif

#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif

#ifndef tbi
#define tbi(port,bit) (port) ^= (1 << (bit))
#endif

int main() {
	ClasseTimer::init();
	Serial<0>::init();
	
	Balise & balise = Balise::Instance();
	Serial<0>::change_baudrate(9600);
	
	//Initialisation table pour crc8
	init_crc8();
 	
 	//Pin21 = input impulsion compte tour
	//Activation des interruptions sur front montant pour pin 21 sur board Arduino
	sbi(EICRA,ISC01);//Configuration front montant
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite

	// Initialisation interruptions codeurs
	// Masques
	//PCMSK0 |= (1 << PCINT7);
	// Activer les interruptions
	//PCICR |= (1 << PCIE0);
	
	sei();

	unsigned char rawFrame[3];
	
	while (1) {		
		
		Serial<0>::read(rawFrame,4);
		Frame frame(rawFrame);

		if (frame.isValid()) {
			
			Serial<0>::print(frame.getRobotId());
			Serial<0>::print(frame.getDistance());
			//Serial<0>::print(balise.getAngle());
		} else {
			Serial<0>::print("ERROR");
		}
	}
}

ISR(TIMER0_OVF_vect)
{
	Balise & balise = Balise::Instance();
	balise.incremente_toptour();
}

//INT0
ISR(INT0_vect)
{
	Balise & balise = Balise::Instance();
	if(balise.toptour()>=100)
		balise.max_counter(balise.toptour());
	balise.reset_toptour();
}
