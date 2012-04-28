#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>
#include <libintech/ultrason.hpp>

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
	Serial<0>::change_baudrate(57600);
	//Pin D2 en INPUT
	cbi(DDRD,DD2);
	//Pin D7 en INPUT
	cbi(DDRD,PD7);
	cbi(PORTD,PD7);//Pull up disabled
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
		Serial<0>::read(buffer,17);

		#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

		if(COMPARE_BUFFER("?",1)){
			Serial<0>::print(1);
		}
		if(COMPARE_BUFFER("ultrason",8)){
			Serial<0>::print(max(ultrason_g.value(),ultrason_d.value()));
		}
		if(COMPARE_BUFFER("jumper",6)){
			Serial<0>::print(rbi(PIND,PD7));
		}
	}
	
	return 0;
}

ISR(TIMER1_OVF_vect){
	asm("nop");
}


