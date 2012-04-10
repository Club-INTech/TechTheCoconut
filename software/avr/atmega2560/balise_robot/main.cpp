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

#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

#define READ_CANAL_A() rbi(PINB,PORTB4)
#define READ_CANAL_B() rbi(PINB,PORTB5)

volatile uint8_t dernier_etat_a;
volatile uint8_t dernier_etat_b;
volatile int32_t codeur;
volatile int32_t last_codeur = 0;

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
	// Interruptions de codeuse(PCINT4 => Pin 10 sur l'Arduino)
	sbi(PCMSK0,PCINT4);
	// Activer les interruptions
	sbi(PCICR,PCIE0);

	// Initialisation interruptions codeurs
	// Masques
	//PCMSK0 |= (1 << PCINT7);
	// Activer les interruptions
	//PCICR |= (1 << PCIE0);
	
	sei();

	unsigned char rawFrame[3];
	
	while (1) {
// 		Serial<0>::read(rawFrame,4);
		Serial<0>::print(0);
 		/*Serial<0>::read(rawFrame,4);
 		Frame frame(rawFrame);
 
 		if(frame.isValid()){
 			
 			//Serial<0>::print(frame.getRobotId());
 			Serial<0>::print(frame.getDistance());
 			//Serial<0>::print(balise.getAngle());
 		} else {
 			Serial<0>::print("ERROR");
 		}*/
	}
	
}

ISR(TIMER0_OVF_vect)
{
	Balise::Instance().incremente_toptour();
	Balise::Instance().asservir(codeur - last_codeur);
}

ISR(TIMER1_OVF_vect)
{
	//Serial<0>::print(codeur - last_codeur);
	Balise::Instance().asservir(codeur - last_codeur);
	last_codeur = codeur;
}

//INT0
ISR(INT0_vect)
{
	Balise & balise = Balise::Instance();
	if(balise.toptour()>=100)
		balise.max_counter(balise.toptour());
	balise.reset_toptour();
}

ISR(PCINT0_vect)
{
	 if(dernier_etat_a == 0 && READ_CANAL_A() == 1){
	   if(READ_CANAL_B() == 0)
	     codeur--;
	   else
	     codeur++;
	 }
	 else if(dernier_etat_a == 1 && READ_CANAL_A() == 0){
	   if(READ_CANAL_B() == 0)
	     codeur++;
	   else
	     codeur--;
	 }
	 else if(dernier_etat_b == 0 && READ_CANAL_B() == 1){
	   if(READ_CANAL_A() == 0)
	     codeur--;
	   else
	     codeur++;
	 }
	 else if(dernier_etat_b == 1 && READ_CANAL_B() == 0){
	   if(READ_CANAL_A() == 0)
	     codeur++;
	   else
	     codeur--;
	 }
	dernier_etat_a = READ_CANAL_A();
	dernier_etat_b = READ_CANAL_B(); 
}
