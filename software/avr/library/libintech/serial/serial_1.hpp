/*
 * serial_1.hpp
 *
 *  Created on: 7 févr. 2012
 *      Author: philippe
 */

#ifndef SERIAL_1_HPP_
#define SERIAL_1_HPP_

#if defined (__AVR_ATmega640__)\
	|| defined (__AVR_ATmega1280__)\
	|| defined (__AVR_ATmega1281__)\
	|| defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)

	#define INIT_BAUDRATE_1 57600
	#include <libintech/serial/serial_impl.hpp>

	template<>
	void Serial<1>::init(){
		static bool is_init = false;
		if(is_init == false){
			uint16_t UBRR  =(F_CPU/8/INIT_BAUDRATE_1 - 1)/2;
			UBRR1H = (unsigned char)(UBRR >> 8);
			UBRR1L = (unsigned char)UBRR;
			UCSR1C = (1 << USBS1)|(3<<UCSZ10);
			UCSR1B |= ( 1 << RXCIE1 );	//Activation de l'interruption de réception
			UCSR1B |= ( 1 << RXEN1 );	//Activation de la réception
			UCSR1B |= ( 1 << TXEN1 );	//Activation de l'emission
			is_init = true;
		}
	}
	
	template<>
	void Serial<1>::send_char(unsigned char byte)
	{
			init();
	        while ( !( UCSR1A & (1<<UDRE1)) );
	        UDR1 = byte;
	}

	template<>
	void Serial<1>::change_baudrate(uint32_t new_baudrate){
		init();
		uint16_t UBRR  =(F_CPU/8/new_baudrate - 1)/2;
		UBRR1H = (unsigned char)(UBRR >> 8);
		UBRR1L = (unsigned char)UBRR;
		UCSR1C = (1 << USBS1)|(3<<UCSZ10);
	}




	ISR(USART1_RX_vect)
	{
		unsigned char c = UDR1;
		Serial<1>::store_char(c);
	}

#endif


#endif /* SERIAL_1_HPP_ */
