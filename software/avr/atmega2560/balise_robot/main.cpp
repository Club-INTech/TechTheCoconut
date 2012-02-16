#include <libintech/serial/serial_0.hpp>
#include <libintech/timer.hpp>

#include <stdint.h>
#include <avr/delay.h>
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

//  #include <libintech/serial/serial_1.hpp>
//  #include <libintech/serial/serial_2.hpp>
//  #include <libintech/serial/serial_3.hpp>


int main() {
	Serial < 0 > &serial0 = Serial < 0 > ::Instance();
	ClasseTimer &angle_counter = ClasseTimer::Instance();
	Balise & balise = Balise::Instance();
	
	serial0.change_baudrate(9600);
	//Initialisation table pour crc8
	init_crc8();
	//Pin B0 en input (Pin 53 sur board Arduino)
	cbi(DDRB, PORTB0);
	//Pin B1 en input (Pin 52 sur board Arduino)
	sbi(DDRB, PORTB1);
	//Activation interruption INT0 sur front montant
	sbi(EICRA,ISC01);//Configuration front montant
	sbi(EICRA,ISC00);
	sbi(EIMSK,INT0);//Activation proprement dite
	
	//sei();

	//   Serial<1> & serial1 = Serial<1>::Instance();
	//   Serial<2> & serial2 = Serial<2>::Instance();
	//   Serial<3> & serial3 = Serial<3>::Instance();

	uint32_t rawFrame;
	
	
	while (1) {
		
		serial0.print(42);
		//sbi(PORTB, PORTB1);
		//cbi(PORTB, PORTB1);
		_delay_ms(2000);
		
		/*
		rawFrame = serial0.read<uint32_t>();
		Frame frame(rawFrame);
		if (frame.isValid()) {
			serial0.print(frame.getRobotId());
			serial0.print(frame.getDistance());
			serial0.print(balise.getAngle());
		} else {
			serial0.print("ERROR");
		}*/
	}
}

//INT0
ISR(INT0_vect)
{
	Serial < 0 > &serial0 = Serial < 0 > ::Instance();
	ClasseTimer &angle_counter = ClasseTimer::Instance();
	Balise & balise = Balise::Instance();
	
	serial0.print(balise.getAngle());
	angle_counter.value(0);
}

//#define BAUD 9600
//#define MYUBRR (F_CPU/16)/BAUD-1

//#include <stdint.h>
//#include <string.h>
//#include <avr/pgmspace.h>
//#include <avr/io.h>
//#include <avr/interrupt.h>
//#include <util/delay.h>
//#include <util/setbaud.h>

//void USART_Init(unsigned int ubrr);
//void USART_Transmit(unsigned char data);

//int main(void)
//{
//   USART_Init(16); //MYUBRR = 51 for current settings

//   while(1)
//   {
//      USART_Transmit('A');
//     _delay_ms(500);
//   }
//}

//void USART_Init( unsigned int ubrr)
//{
//   /* Set baud rate */
//   UBRR0H = (unsigned char)(ubrr>>8);
//   UBRR0L = (unsigned char)ubrr;

//   /* Enable receiver and transmitter */
//   UCSR0B = (1<<RXEN0)|(1<<TXEN0);
//   /* Set frame format: 8data, 2stop bit */
//  // UCSR0C = (1<<USBS0)|(3<<UCSZ00);

//    UCSR0C = (!(1<<USBS0))|(1<<UCSZ01)|(1<<UCSZ00);
//}

//void USART_Transmit(unsigned char data)
//{
//   /* Wait for empty transmit buffer */
//   while ( !( UCSR0A & (1<<UDRE0)) );
//   /* Put data into buffer, sends the data */
//   UDR0 = data;
//}
