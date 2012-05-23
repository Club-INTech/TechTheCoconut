#include "main.h"
#include <libintech/timer.hpp>
#include "watchdog.h"

volatile uint8_t WINDOW_OPENER = 0;
volatile uint8_t WINDOW_FLAG = 0;
volatile uint8_t portchistory = 0xFF;
volatile uint8_t changedbits=0;
volatile uint16_t distance = 0;
volatile int32_t message = 0;
volatile int16_t timer=0;
volatile uint32_t timestamp=0;

typedef Timer<0,ModeCounter,1024> window_timer;
typedef Timer<1,ModeCounter,64> timeout_timer;

int main() 
{
    
 	setup();
	
	while(1){
		unsigned char order= Serial<0>::read_char();
		if(order=='v'){

			uint16_t offset=timeout_timer::value();
			Serial<0>::print_noln(distance);
			Serial<0>::print_noln(offset);
			uint32_t data = (((uint32_t) distance) << 16) + offset;
			Serial<0>::print_noln((int) crc8(data));
		}
		else if(order=='t')
		{
		    Serial<0>::print_noln(timer);
		}
		else if(order=='?'){
			Serial<0>::print_noln(40);
		}
		else if(order=='s')
		{
		    uint32_t t1=0,t1prime=0,t2prime=0,t2=0;
		    // Timeout pour la requête de 0,25s
		    WDT_set_prescaler();
		    // Activation du watchdog en mode system reset
		    WDT_on();
		    
		    Serial<0>::print_noln(timestamp);
		    
		    t2prime=Serial<0>::read_int();
		    t2=timestamp;//timesptamp devrait être mis dans t2 avant même la lecture de t2prime
		    t1=Serial<0>::read_int();
		    t1prime=Serial<0>::read_int();
		    //Update du timestamp local
		    timestamp+=(t1prime+t2prime-t1-t2)/2;
		    
		    // Désactivation du watchdog
		    WDT_off();
		}
	}
	
	return 0;
}

void setup()
{
    sbi(DDRD,DDD2);
    sbi(PORTD,PORTD2);
    
	//Pins en input pour les PCINT
	cbi(DDRC,DDC0);
	cbi(DDRC,DDC1);
	cbi(DDRC,DDC2);
	cbi(DDRC,DDC3);
	
	//Pull up enabled
	sbi(PORTC,PORTC0);
	sbi(PORTC,PORTC1);
	sbi(PORTC,PORTC2);
	sbi(PORTC,PORTC3);

	//Active les PCINT
	sbi(PCMSK1,PCINT8);
	sbi(PCMSK1,PCINT9);
	sbi(PCMSK1,PCINT10);
	sbi(PCMSK1,PCINT11);
	sbi(PCICR,PCIE1);//active PCINT port C
	
	//Active globalement les interruptions
	sei();
	
	//Initialisation série
	Serial<0>::init();
	Serial<0>::change_baudrate(9600);
	//Initialisation table pour crc8
	init_crc8();
	timeout_timer::init();
	window_timer::init();
}

//Interruption pour les PCINT8,9,10,11
ISR(PCINT1_vect)
{
    changedbits = PINC ^ portchistory;//masque
    portchistory = PINC;

    //Si front montant
    if((PINC & changedbits)!=0)
    {
		//Si on est dans une fenêtre encore active
		if(WINDOW_FLAG)
		{			
			if(TCNT0*16>=TIME_THRESHOLD_MIN)
			{		
				if(changedbits == WINDOW_OPENER)
				{
					WINDOW_FLAG = 0;
					distance=getDistance(window_timer::value());
					timer=window_timer::value();
					timeout_timer::value(0);
				}
			}
		}
		else
		{
			//On ouvre une fenêtre et initialise le TIMER0
			WINDOW_FLAG = 1;
			window_timer::value(0);
			WINDOW_OPENER=changedbits;
		}
	}
}

//Interruption du TIMER0 sur overflow
ISR(TIMER0_OVF_vect)
{
	//On ferme la fenêtre
	WINDOW_FLAG = 0;
}

ISR(TIMER1_OVF_vect)
{
	timestamp++;
 	distance = 0; //La distance est périmée.
}