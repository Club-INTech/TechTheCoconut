#ifndef REGISTER_HPP_
#define REGISTER_HPP_

#include <stdint.h>
#include <avr/io.h>

/// PORT D
template<uint16_t bit>
struct AVR_PORTD
{
    static void set_input(){
        DDRD &= ~(1 << bit);
    }
    static void set_output(){
        DDRD |= (1 << bit);
    }
    static void set(){
        PORTD |= (1 << bit);
    }
    static void clear(){
        PORTD &= ~(1 << bit);
    }
    static uint8_t read(){
        return ( (PIND & (1 << bit)) >> bit );
    }
};

/// PORT C
template<uint16_t bit>
struct AVR_PORTC
{
    static void set_input(){
        DDRC  &= ~(1 << bit);
    }
    
    static void set_output(){
        DDRC |= (1 << bit);
    }
    
    static void set(){
        PORTC |= (1 << bit);
    }
    
    static void clear(){
        PORTC &= ~(1 << bit);
    }
    
    static uint8_t read(){
        return ( (PINC & (1 << bit)) >> bit );
    }
    
};


/// PORT B
template<uint16_t bit>
struct AVR_PORTB
{
    static void set_input(){
        DDRB  &= ~(1 << bit);
    }
    
    static void set_output(){
        DDRB |= (1 << bit);
    }
    
    static void set(){
        PORTB |= (1 << bit);
    }
    
    static void clear(){
        PORTB &= ~(1 << bit);
    }
    
    static uint8_t read(){
        return ( (PINB & (1 << bit)) >> bit );
    }
    
};

#endif /* REGISTER_HPP_ */
