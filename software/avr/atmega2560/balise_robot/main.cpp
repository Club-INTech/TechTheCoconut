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

//  #include <libintech/serial/serial_1.hpp>
//  #include <libintech/serial/serial_2.hpp>
//  #include <libintech/serial/serial_3.hpp>


int main() {
	ClasseTimer::init();
	Serial<0>::init();
	Balise & balise = Balise::Instance();
	Serial<0>::change_baudrate(9600);
	//Initialisation table pour crc8
	init_crc8();
// 	//Pin B0 en input (Pin 53 sur board Arduino)
// 	cbi(DDRB, PORTB0);
// 	//Pin B1 en input (Pin 52 sur board Arduino)
// 	sbi(DDRB, PORTB1);
	//Activation interruption INT0 sur front montant
// 	sbi(EICRA,ISC01);//Configuration front montant
// 	sbi(EICRA,ISC00);
// 	sbi(EIMSK,INT0);//Activation proprement dite

	// Initialisation interruptions codeurs
	// Masques
	PCMSK0 |= (1 << PCINT7);
	// Activer les interruptions
	PCICR |= (1 << PCIE0);
	
	sei();

	//   Serial<1> & serial1 = Serial<1>::Instance();
	//   Serial<2> & serial2 = Serial<2>::Instance();
	//   Serial<3> & serial3 = Serial<3>::Instance();

	uint32_t rawFrame;
	
	
	while (1) {
// 		cli();		
		
// 		sei();
		Serial<0>::read_int();
		Serial<0>::print(balise.getAngle());
// 		serial0.print("aaaa");
// 		sbi(PORTB, PORTB1);
// 		_delay_ms(2000);
// 		cbi(PORTB, PORTB1);
// 		
		
		/*
		rawFrame = serial0.read<uint32_t>();
		Frame frame(rawFrame);
		if (frame.isValid()) {
			serial0.print(frame.getRobotId());
			serial0.print(frame.getDistance());
			serial0.print(balise.getAngle());
		} else {
			serial0.print("ERROR");
		}*/
	}
}

//INT0
ISR(TIMER1_OVF_vect)
{

	
}


ISR(PCINT0_vect)
{
	Balise & balise = Balise::Instance();
	balise.max_counter(ClasseTimer::value());
	ClasseTimer::value(0);
}

