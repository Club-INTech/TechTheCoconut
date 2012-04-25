#include <avr/io.h> 
#include <avr/interrupt.h>
#include <util/delay.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

#include "infrarouge.h"



typedef Serial<0> serial_t_;

int main (void) 
{ 
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    
    
    
//    DDRE |= (1 << 2); // Set LED1 as output 
//    DDRG |= (1 << 0); // Set LED2 as output 

   ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescalar to 128 - 125KHz sample rate @ 16MHz 

   ADMUX |= (1 << REFS0); // Set ADC reference to AVCC 
   ADMUX |= (1 << ADLAR); // Left adjust ADC result to allow easy 8 bit reading 

   // No MUX values needed to be changed to use ADC0 
    
   ADCSRA |= (1 << 5);  // Set ADC to Free-Running Mode 
   ADCSRA |= (1 << ADEN);  // Enable ADC 
   ADCSRA |= (1 << ADSC);  // Start A2D Conversions 

   for(;;)  // Loop Forever 
   { 
        serial_t_::print(ADCH);

        serial_t_::print(conversion(ADCH));
        serial_t_::print("***********");
        _delay_ms(100);   
   } 

} 

