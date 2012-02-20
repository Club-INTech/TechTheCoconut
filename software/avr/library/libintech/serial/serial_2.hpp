/*
 * serial_2.hpp
 *
 *  Created on: 7 févr. 2012
 *      Author: philippe
 */

#ifndef SERIAL_2_HPP_
#define SERIAL_2_HPP_




#if defined (__AVR_ATmega640__)\
	|| defined (__AVR_ATmega1280__)\
	|| defined (__AVR_ATmega1281__)\
	|| defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)

#include <libintech/serial/serial_impl.hpp>
#define INIT_BAUDRATE_2 57600


	template<>
	void Serial<2>::init(){
		Serial<2>::PLEASE_INCLUDE_SERIAL_INTERRUPT();
		static bool is_init = false;
		if(is_init == false){
			uint16_t UBRR  = (F_CPU/8/INIT_BAUDRATE_2 - 1)/2;
			UBRR2H = (unsigned char)(UBRR >> 8);
			UBRR2L = (unsigned char)UBRR;
			UCSR2C = (1 << USBS2)|(3<<UCSZ20);
			UCSR2B |= ( 1 << RXCIE2 );	//Activation de l'interruption de réception
			UCSR2B |= ( 1 << RXEN2 );	//Activation de la réception
			UCSR2B |= ( 1 << TXEN2 );	//Activation de l'emission
			is_init = true;
		}
	}

	template<>
	void Serial<2>::send_char(unsigned char byte)
	{
			init();
	        while ( !( UCSR2A & (1<<UDRE2)) );
	        UDR2 = byte;
	}

	template<>
	void Serial<2>::change_baudrate(uint32_t new_baudrate){
		init();
		uint16_t UBRR  =(F_CPU/8/new_baudrate - 1)/2;
		UBRR2H = (unsigned char)(UBRR >> 8);
		UBRR2L = (unsigned char)UBRR;
		UCSR2C = (1 << USBS2)|(3<<UCSZ20);
	}


	ISR(USART2_RX_vect)
	{
		unsigned char c = UDR2;
		Serial<2>::store_char(c);
	}

#endif


#endif /* SERIAL_2_HPP_ */
