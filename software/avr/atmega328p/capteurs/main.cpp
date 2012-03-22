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
typedef Serial<0> serial_t_;
ring_buffer<uint16_t, 3> mesures_g;
ring_buffer<uint16_t, 3> mesures_d;
uint16_t derniere_valeur_g;
uint16_t derniere_valeur_d;

int compare (const void * a, const void * b)
{
  return ( *(uint16_t*)a - *(uint16_t*)b );
}

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
	  	char buffer[17];
		uint8_t length = serial_t_::read(buffer,17);

	#define COMPARE_BUFFER(string) strncmp(buffer, string, length) == 0 && length>0

		if(COMPARE_BUFFER("?")){
			serial_t_::print(1);
		}

		if(COMPARE_BUFFER("ultrason")){
			cli();
			qsort(mesures_d.data(),mesures_d.size(),sizeof(uint16_t),compare);
			qsort(mesures_g.data(),mesures_g.size(),sizeof(uint16_t),compare);
			serial_t_::print(max(mesures_g.data()[mesures_g.size()/2],mesures_d.data()[mesures_d.size()/2]));
			sei();
		}

// 		for(int i=0; i<mesures_d.size(); ++i){
// 		  Serial<0>::print(mesures_d.data()[i]);
// 		}
// 		qsort(mesures_g.data(),mesures_g.size(),sizeof(uint16_t),compare);
// 		for(int i=0; i<mesures_g.size(); ++i){
// 		  Serial<0>::print(mesures_g.data()[i]);
// 		}
// 		Serial<0>::print("Mediane");
		
// 		Serial<0>::print("\n\n\n\n");
	}
	
	return 0;
}

ISR(INT0_vect)
{
	//Front montant
	if(rbi(PIND,PORTD2)){
		derniere_valeur_g = ClasseTimer::value();
	}else{//Front descendant
		// prescaler/fcpu*inchToCm/tempsParInch
		if(ClasseTimer::value() <derniere_valeur_g)
		  mesures_g.append((ClasseTimer::value() + 65536 - derniere_valeur_g  )*0.0884353741496);
		else
		  mesures_g.append((ClasseTimer::value() - derniere_valeur_g )*0.0884353741496);
	}
}

ISR(INT1_vect)
{
	//Front montant
	if(rbi(PIND,PORTD3))	{
		derniere_valeur_d = ClasseTimer::value();
	}else{//Front descendant
		// prescaler/fcpu*inchToCm/tempsParInch
		if(ClasseTimer::value() < derniere_valeur_d)
		  mesures_d.append((ClasseTimer::value() + 65536 - derniere_valeur_d  )*0.0884353741496);
		else
		  mesures_d.append((ClasseTimer::value() - derniere_valeur_d )*0.0884353741496);
	}
}

ISR(TIMER1_OVF_vect){
}


