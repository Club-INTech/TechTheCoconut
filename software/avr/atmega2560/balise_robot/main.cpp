#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_1_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/serial/serial_1.hpp>
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

typedef Serial<1> serial_radio;
typedef Serial<0> serial_pc;
int main() {
	
	Balise & balise = Balise::Instance();
	init();

	//unsigned char rawFrame[3];
	uint32_t rawFrame=0;
	
	while (1) {
		
		char buffer[10];
		serial_pc::read(buffer,10);
		
		#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

		if(COMPARE_BUFFER("?",1)){
			serial_pc::print(2);
		}
// 		
		if(COMPARE_BUFFER("!",1)){
			bool is_valid = false;
			Frame frame(0);
			const int val=10;
// 			serial_pc::print(val);
			serial_radio::print(val);
			serial_pc::print(serial_radio::read_int());
// 			do{
// // 				serial_radio::synchronize();
// 				rawFrame=serial_radio::read_int();
// 				serial_pc::print(rawFrame);
// 				frame = rawFrame;
// 				is_valid = frame.isValid();
// 				serial_radio::print(is_valid);
// 			}while(is_valid==false);
// 			serial_pc::print(frame.getRobotId());
// 			serial_pc::print(frame.getDistance());
// 			serial_pc::print((uint16_t)balise.getAngle());
		}
		#undef COMPARE_BUFFER
	}
	
}

void init()
{
  	ClasseTimer::init();
	serial_pc::init();
	serial_pc::change_baudrate(9600);
	serial_radio::init();
	serial_radio::change_baudrate(9600);
	
	//5V sur la pin 12 (B6) pour la direction laser
	sbi(DDRB,PORTB6);
	sbi(PORTB,PORTB6);
	//On met la pin 13 (OC0A, B7) en OUT
	sbi(DDRB,PORTB7);

	//Config PWM de la pin 13 (créneau de 40Hz)
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
// 	Balise::Instance().asservir(codeur - last_codeur);
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
