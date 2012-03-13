#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>

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
ring_buffer<unsigned int, 6> mesures;
uint16_t derniere_valeur1;
uint16_t derniere_valeur2;

int main() {

	ClasseTimer::init();
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
	}
	
	return 0;
}

ISR(INT0_vect)
{
	//Front montant
	if(rbi(PIND,PORTD2)){
		derniere_valeur1 = ClasseTimer::value();
	}else{//Front descendant
		// prescaler/fcpu*inchToCm/tempsParInch
		if(ClasseTimer::value() < derniere_valeur1)
		  mesures.append(uint16_t((ClasseTimer::value() + 65536 - derniere_valeur1  )*0.0884353741496));
		else
		  mesures.append(uint16_t((ClasseTimer::value() - derniere_valeur1 )*0.0884353741496));
		Serial<0>::print(mesures.data()[mesures.current() - 1]);
	}
}

ISR(INT1_vect)
{
	//Front montant
	if(rbi(PIND,PORTD3))	{
		derniere_valeur2 = ClasseTimer::value();
	}else{//Front descendant
		// prescaler/fcpu*inchToCm/tempsParInch
		if(ClasseTimer::value() < derniere_valeur2)
		  mesures.append(uint16_t((ClasseTimer::value() + 65536 - derniere_valeur2  )*0.0884353741496));
		else
		  mesures.append(uint16_t((ClasseTimer::value() - derniere_valeur2 )*0.0884353741496));
		Serial<0>::print(mesures.data()[mesures.current() - 1]);
	}
}

ISR(TIMER1_OVF_vect){
}


