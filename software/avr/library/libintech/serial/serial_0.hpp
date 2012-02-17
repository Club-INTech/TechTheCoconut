#ifndef SERIAL_0_HPP_
#define SERIAL_0_HPP_

#include <libintech/serial/serial_impl.hpp>

#define INIT_BAUDRATE_0 57600

template<>
inline void Serial<0>::init(){
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

#if defined (__AVR_ATmega328P__) || defined (__AVR_ATmega328__)
ISR( inline USART_RX_vect)
#elif defined (__AVR_ATmega640__)\
		|| defined (__AVR_ATmega1280__)\
		|| defined (__AVR_ATmega1281__)\
		|| defined (__AVR_ATmega2560__)\
		|| defined (__AVR_ATmega2561__)
ISR( inline USART0_RX_vect)
#endif
{
	unsigned char c = UDR0;
	Serial<0>::store_char(c);
}

#endif /* SERIAL_0_HPP_ */
