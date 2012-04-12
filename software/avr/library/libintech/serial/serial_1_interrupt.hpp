#ifndef SERIAL_1_INTERRUPT_HPP
#define SERIAL_1_INTERRUPT_HPP
#include <stdint.h>

#include "serial_impl.hpp"

	template<>
	void Serial<1>::PLEASE_INCLUDE_SERIAL_INTERRUPT()
	{
		
	}
	
	#if defined (__AVR_ATmega640__)\
	|| defined (__AVR_ATmega1280__)\
	|| defined (__AVR_ATmega1281__)\
	|| defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)\
	|| defined (__AVR_ATmega324P__)
	ISR( USART1_RX_vect)
	#endif
	{
		unsigned char c = UDR1;
		Serial<1>::store_char(c);
	}
	

#endif