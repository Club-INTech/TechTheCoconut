#include "main.h"

volatile uint8_t WINDOW_OPENER = 0;
volatile uint8_t WINDOW_FLAG = 0;
volatile uint8_t portchistory = 0xFF;
volatile uint8_t changedbits=0;
volatile int16_t distance = 0;

int main() 
{
 	setup();
	
	while(1){
		char buffer[10];
		int16_t order = 0;
// 		Serial<0>::read(order);
		Serial<0>::print(order);
// 		if(order==1){
// 			sendData(distance);
// 			int16_t ACK=0;
// 			do{
// 				sendData(distance);
// 				ACK = Serial<0>::read_int();
// 			}while(ACK!=1);
// 		}
	}
	
	return 0;
}

void setup()
{
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
	
	//Réglages du TIMER0
	//Prescaler de 256
	sbi(TCCR0B,CS02);
	cbi(TCCR0B,CS01);
	cbi(TCCR0B,CS00);
	//Active interruptions sur overflow du TIMER0
	sbi(TIMSK0,TOIE0);
	
	//Active globalement les interruptions
	sei();
	
	//Initialisation série
	Serial<0>::init();
	Serial<0>::change_baudrate(9600);
	//Initialisation table pour crc8
	init_crc8();
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
			Frame message;
		
			if(TCNT0*16>=TIME_THRESHOLD_MIN)
			{		
				if(changedbits == WINDOW_OPENER)
				{
					WINDOW_FLAG = 0;
					distance=getDistance(TCNT0*16);//TCNT0*16 = écart de temps en µs
// 					message=makeFrame(distance);
// 					sendFrame(message);
				}
			}
		}
		else
		{
			//On ouvre une fenêtre et initialise le TIMER0
			WINDOW_FLAG = 1;
			TCNT0=0;
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
