#include "main.h"
#include <libintech/timer.hpp>

volatile int8_t overflow1= 0;
volatile int8_t overflow2 = 0;
volatile int8_t overflow3 = 0;
volatile int8_t overflow4 = 0;

volatile int16_t window1 = -1;
volatile int16_t window2 = -1;
volatile int16_t window3 = -1;
volatile int16_t window4 = -1;

volatile uint8_t portchistory = 0xFF;
volatile uint8_t changedbits=0;
volatile uint16_t distance = 0;
volatile int16_t timer=13;

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
	switch(changedbits)
	{
	  case 8:
	    //Si fenêtre fermée
	    if(window4==-1)
	    {//Ouverture de la fenêtre
	      window4=window_timer::value();
	      overflow4=0;
	    }
	    else
	    {
		uint8_t time=window_timer::value()-window4+255*overflow4;
		if(time>=TIME_THRESHOLD_MIN)
		{
		  distance=getDistance(time);
		  timer=time;
		  //On ferme les fenêtres
		  window1=-1;
		  window2=-1;
		  window3=-1;
		  timeout_timer::value(0);//Démarre le timer de validité
		  
		}
	      
	      //Fermeture de cette fenêtre
	      window4=-1;
	    }
	    break;
	}
    }
}

//Interruption du TIMER0 sur overflow
ISR(TIMER0_OVF_vect)
{
      if(window4!=-1)
      {
	if(overflow4<50)
	   overflow4++;
	else
	  window4=-1;
      }
}

ISR(TIMER1_OVF_vect)
{
 	distance = 0; //La distance est périmée.
}