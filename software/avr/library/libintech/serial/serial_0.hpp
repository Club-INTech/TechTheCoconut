#ifndef SERIAL_0_HPP_
#define SERIAL_0_HPP_

#include <libintech/serial/serial_impl.hpp>

#define USE_SERIAL_0
#define INIT_BAUDRATE_0 57600

template<>
inline void Serial<0>::init(){
	Serial<0>::PLEASE_INCLUDE_SERIAL_INTERRUPT();
	static bool is_init = false;
	if(is_init == false){
		uint16_t UBRR  =(F_CPU/8/INIT_BAUDRATE_0 - 1)/2;
		UBRR0H = (unsigned char)(UBRR >> 8);
		UBRR0L = (unsigned char)UBRR;
		UCSR0C = (1 << USBS0)|(3<<UCSZ00);
		UCSR0B |= ( 1 << RXCIE0 );	//Activation de l'interruption de réception
		UCSR0B |= ( 1 << RXEN0 );	//Activation de la réception
		UCSR0B |= ( 1 << TXEN0 );	//Activation de l'emission
		is_init = true;
	}
}

template<>
inline void Serial<0>::send_char(unsigned char byte)
{
	while ( !( UCSR0A & (1<<UDRE0)) );
	UDR0 = byte;
}

template<>
inline void Serial<0>::change_baudrate(uint32_t new_baudrate){
	uint16_t UBRR  =(F_CPU/8/new_baudrate - 1)/2;
	UBRR0H = (unsigned char)(UBRR >> 8);
	UBRR0L = (unsigned char)UBRR;
	UCSR0C = (1 << USBS0)|(3<<UCSZ00);
}

#endif /* SERIAL_0_HPP_ */
