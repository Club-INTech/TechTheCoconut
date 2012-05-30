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
#include "watchdog.h"
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
/*
#define READ_CANAL_A() rbi(PINB,PORTB4)
#define READ_CANAL_B() rbi(PINB,PORTB5)*/

void init();

volatile uint8_t dernier_etat_a;
volatile uint8_t dernier_etat_b;
volatile int32_t codeur;
volatile int32_t last_codeur = 0;

int main() {
	
	Balise & balise = Balise::Instance();
	init(); 
	balise.moteur_on();
	balise.laser_on();
	// En cas de reset par le watchdog
	if (WDT_is_reset())
	{
		// Envoi du timeout au PC
		Balise::serial_pc::print("timeout");
        
		// Désactivation du watchdog
		WDT_off();
	}
    uint8_t n_lu_prec = 0;
	while (1) {
		char buffer[10];
		uint8_t n_lu = Balise::Balise::serial_pc::read(buffer,10);
		if(n_lu == 0) n_lu = n_lu_prec;
		#define COMPARE_BUFFER(string,len) (len==n_lu && strncmp(buffer, string, n_lu) == 0 && n_lu>0) 

		//Ping
		if(COMPARE_BUFFER("?",1)){
			Balise::serial_pc::print(2);
		}
		
		if(COMPARE_BUFFER("allumer",7)){
            balise.moteur_on();
            balise.laser_on();
        }
        
        if(COMPARE_BUFFER("eteindre",8)){
            balise.moteur_off();
            balise.laser_off();
        }
		//Speed
		if(COMPARE_BUFFER("s",1)){
			Balise::serial_pc::print(balise.max_counter());
		}
		
		//Laser off
		if(COMPARE_BUFFER("loff",4)){
		    balise.laser_off();
		}
		
		//Laser on
		if(COMPARE_BUFFER("lon",3)){
		    balise.laser_on();
		}		    

		//Ping balise adverse
		if(COMPARE_BUFFER("!",1)){
			// Timeout pour la requête de 0,25s
			WDT_set_prescaler();
			
			// Activation du watchdog en mode system reset
			WDT_on();
			
			// Envoi du ping à la balise
			Balise::serial_radio::print_noln('?');
			Balise::serial_pc::print(Balise::serial_radio::read_int());
			
			// Désactivation du watchdog
			WDT_off();
		}
		
		//Table
		if(COMPARE_BUFFER("t",1)){
			// Timeout pour la requête de 0,25s
			WDT_set_prescaler();
			
			// Activation du watchdog en mode system reset
			WDT_on();
			
			// Envoi du ping à la balise
			Balise::serial_radio::print_noln('t');
			Balise::serial_pc::print(Balise::serial_radio::read_int());
			
			// Désactivation du watchdog
			WDT_off();
		}
		
		//Valeurs
		if(COMPARE_BUFFER("v",1)){
			bool is_valid = false;
			int16_t n_demandes = 0;
			int32_t distance;
			int32_t offset = 0;
			int32_t angle = 0;
			int32_t crc;
			do{
				// Timeout pour la requête de 0,25s
				WDT_set_prescaler();
			
				// Activation du watchdog en mode system reset
				WDT_on();
				
				// Envoi à la balise d'une demande de mise à jour
				Balise::serial_radio::print_noln('v');
				
				//Calcul du temps des read pour correction de l'offset
				int32_t t1 = Balise::T_TopTour::value();
				distance = Balise::serial_radio::read_int();
				offset = Balise::serial_radio::read_int();
				crc = Balise::serial_radio::read_int();
				int32_t t2 = Balise::T_TopTour::value();			
				
				if(t2 < t1){
				  t2+=balise.max_counter();
				}
 				angle = balise.getAngle(offset + (t2 - t1)*5/4);
				is_valid = (crc==((int32_t) crc8((distance << 16) + offset)));

				n_demandes++;
			}while(is_valid==false && n_demandes<5);
			
			// Désactivation du watchdog
			WDT_off();
			
			if(n_demandes==5){
				Balise::serial_pc::print("ERREUR_CANAL");
			}
			else if(distance==0){
				//Distance écrasée par le timeout côté balise (distance périmée).
				Balise::serial_pc::print("NON_VISIBLE"); 
			}
			else{
				char str[80] = {0};
				char buff[20];
				ltoa(1,buff,10);
				strcat(str,buff);
				strcat(str,".");
				ltoa(distance,buff,10);
				strcat(str,buff);
				strcat(str,".");
				ltoa(angle,buff,10);
				strcat(str,buff);
				Balise::serial_pc::print((const char *)str);
			}
		}
		
		if(COMPARE_BUFFER("mon",3)){
		    balise.moteur_on();
		}
        
		if(COMPARE_BUFFER("moff",4)){
		    balise.moteur_off();
            balise.laser_off();
		}
		//Easter egg
		if(COMPARE_BUFFER("troll",5)){
			Balise::serial_pc::print("MER IL ET FOU ! ENKULE DE RIRE");
		}
		
		#undef COMPARE_BUFFER
		n_lu_prec = n_lu;
	}
	
}

void init()
{	
	//Initialisation table pour crc8
	init_crc8();
 	
 	//Pin21 = input impulsion compte tour
	//Activation des interruptions sur front montant pour pin 21 sur board Arduino
	sbi(EICRA,ISC01);//Configuration front montant
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite

// 	// Initialisation interruptions codeurs
// 	// Interruptions de codeuse(PCINT4 => Pin 10 sur l'Arduino)
// 	sbi(PCMSK0,PCINT4);
// 	// Activer les interruptions
// 	sbi(PCICR,PCIE0);

	// Initialisation interruptions codeurs
	// Masques
	//PCMSK0 |= (1 << PCINT7);
	// Activer les interruptions
	//PCICR |= (1 << PCIE0);
	
	sei();
}




ISR(TIMER1_OVF_vect)
{
	//Serial<0>::print(codeur - last_codeur);
// 	Balise::Instance().asservir(codeur - last_codeur);
// 	last_codeur = codeur;
}

ISR(TIMER3_OVF_vect)
{
}

//INT0
ISR(INT0_vect)
{
	Balise & balise = Balise::Instance();
	//On ignore les impulsions quand l'aimant est encore trop proche du capteur
	if(Balise::T_TopTour::value()>=balise.max_counter()/3){
		balise.max_counter(Balise::T_TopTour::value());
		Balise::T_TopTour::value(0);
	}
}

ISR(PCINT0_vect)
{
// 	 if(dernier_etat_a == 0 && READ_CANAL_A() == 1){
// 	   if(READ_CANAL_B() == 0)
// 	     codeur--;
// 	   else
// 	     codeur++;
// 	 }
// 	 else if(dernier_etat_a == 1 && READ_CANAL_A() == 0){
// 	   if(READ_CANAL_B() == 0)
// 	     codeur++;
// 	   else
// 	     codeur--;
// 	 }
// 	 else if(dernier_etat_b == 0 && READ_CANAL_B() == 1){
// 	   if(READ_CANAL_A() == 0)
// 	     codeur--;
// 	   else
// 	     codeur++;
// 	 }
// 	 else if(dernier_etat_b == 1 && READ_CANAL_B() == 0){
// 	   if(READ_CANAL_A() == 0)
// 	     codeur++;
// 	   else
// 	     codeur--;
// 	 }
// 	dernier_etat_a = READ_CANAL_A();
// 	dernier_etat_b = READ_CANAL_B(); 
}
