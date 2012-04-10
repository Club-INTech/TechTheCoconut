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

void init();

volatile uint8_t dernier_etat_a;
volatile uint8_t dernier_etat_b;
volatile int32_t codeur;
volatile int32_t last_codeur = 0;

int main() {
	
	Balise & balise = Balise::Instance();
	init();

	//unsigned char rawFrame[3];
	uint32_t rawFrame=0;
	
	while (1) {
		rawFrame=Serial<0>::read_int();
		Serial<0>::print(rawFrame);
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

void init()
{
  	ClasseTimer::init();
	Serial<0>::init();
	Serial<0>::change_baudrate(9600);
	
	//5V sur la pin 12 (B6) pour la direction laser
	sbi(DDRB,PORTB6);
	sbi(PORTB,PORTB6);
	//On met la pin 13 (OC0A, B7) en OUT
	sbi(DDRB,PORTB7);

	//Active mode CTC (cf datasheet p 96)
	cbi(TCCR0A,WGM00);
	sbi(TCCR0A,WGM01);
	cbi(TCCR0B,WGM02);

	//Défini le mode de comparaison
	sbi(TCCR0A,COM0A0);
	cbi(TCCR0A,COM0A1);

	// Prescaler (=1)
	cbi(TCCR0B,CS02);
	cbi(TCCR0B,CS01);
	sbi(TCCR0B,CS00);

	//Seuil (cf formule datasheet)
	//f_wanted=16000000/(2*prescaler*(1+OCR0A))
	OCR0A= 199;
	
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
