#ifndef REGISTER_HPP_
#define REGISTER_HPP_

#include <stdint.h>
#include <avr/io.h>

template<uint16_t bit>
struct AVR_PORTD{
	static void set(){
		PORTD |= (1 << bit);
	}
	static void clear(){
		PORTD &= ~(1 << bit);
	}
};

template<uint16_t bit>
struct AVR_PORTB{
	static void set(){
		PORTB |= (1 << bit);
	}
	static void clear(){
		PORTB &= ~(1 << bit);
	}
};

#endif /* REGISTER_HPP_ */
