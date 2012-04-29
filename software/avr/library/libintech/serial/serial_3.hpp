/*
 * serial_3.hpp
 *
 *  Created on: 7 févr. 2012
 *      Author: philippe
 */

#ifndef SERIAL_3_HPP_
#define SERIAL_3_HPP_





#if defined (__AVR_ATmega640__)\
	|| defined (__AVR_ATmega1280__)\
	|| defined (__AVR_ATmega1281__)\
	|| defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)

#include <libintech/serial/serial_impl.hpp>
#define INIT_BAUDRATE_3 57600

	template<>
	void Serial<3>::init(){
		Serial<3>::PLEASE_INCLUDE_SERIAL_INTERRUPT();
		static bool is_init = false;
		if(is_init == false){
			uint16_t UBRR  =(F_CPU/8/INIT_BAUDRATE_3 - 1)/2;
			UBRR3H = (unsigned char)(UBRR >> 8);
			UBRR3L = (unsigned char)UBRR;
			UCSR3C = (1 << USBS3)|(3<<UCSZ30);
			UCSR3B |= ( 1 << RXCIE3 );	//Activation de l'interruption de réception
			UCSR3B |= ( 1 << RXEN3 );	//Activation de la réception
			UCSR3B |= ( 1 << TXEN3 );	//Activation de l'emission
			is_init = true;
		}
	}

	template<>
	void Serial<3>::send_char(unsigned char byte)
	{
			init();
	        while ( !( UCSR3A & (1<<UDRE3)) );
	        UDR3 = byte;
	}

	template<>
	void Serial<3>::change_baudrate(uint32_t new_baudrate){
		init();
		uint16_t UBRR  =(F_CPU/8/new_baudrate - 1)/2;
		UBRR3H = (unsigned char)(UBRR >> 8);
		UBRR3L = (unsigned char)UBRR;
		UCSR3C = (1 << USBS3)|(3<<UCSZ30);
	}

	ISR(USART3_RX_vect)
	{
		unsigned char c = UDR3;
		Serial<3>::store_char(c);
	}

#endif


#endif /* SERIAL_3_HPP_ */
