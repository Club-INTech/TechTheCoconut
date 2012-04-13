#ifndef SERIAL_1_HPP_
#define SERIAL_1_HPP_

#include <libintech/serial/serial_impl.hpp>

#define USE_SERIAL_1
#define INIT_BAUDRATE_1 57600

template<>
inline void Serial<1>::init(){
	Serial<1>::PLEASE_INCLUDE_SERIAL_INTERRUPT();
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
inline void Serial<1>::send_char(unsigned char byte)
{
	while ( !( UCSR1A & (1<<UDRE1)) );
	UDR1 = byte;
}

template<>
inline void Serial<1>::change_baudrate(uint32_t new_baudrate){
	uint16_t UBRR  =(F_CPU/8/new_baudrate - 1)/2;
	UBRR1H = (unsigned char)(UBRR >> 8);
	UBRR1L = (unsigned char)UBRR;
	UCSR1C = (1 << USBS1)|(3<<UCSZ10);
}

#endif /* SERIAL_0_HPP_ */
