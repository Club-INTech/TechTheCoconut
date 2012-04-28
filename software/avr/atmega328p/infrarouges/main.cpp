// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

// LIBRAIRIE LOCALE
#include "infrarouge.h"

//Fonctions de lecture/écriture de bit (utile pour capteurs & jumper)
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif


typedef Serial<0> serial_t_;

int main (void) 
{ 
    serial_t_::init();
    serial_t_::change_baudrate(9600);

   ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescalar to 128 - 125KHz sample rate @ 16MHz 

   ADMUX |= (1 << REFS0); // Set ADC reference to AVCC 
   ADMUX |= (1 << ADLAR); // Left adjust ADC result to allow easy 8 bit reading 

   // No MUX values needed to be changed to use ADC0 
    
   ADCSRA |= (1 << 5);  // Set ADC to Free-Running Mode 
   ADCSRA |= (1 << ADEN);  // Enable ADC 
   ADCSRA |= (1 << ADSC);  // Start A2D Conversions 

   while (1)  // Loop Forever 
   {
        char buffer[17];
        serial_t_::read(buffer,17);
        #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
        
        // ping
        if (COMPARE_BUFFER("?", 1))
            serial_t_::print(5);
            
        if(COMPARE_BUFFER("infra", 5)){
            serial_t_::print(conversion(ADCH));
        }
        
        

   }    
   
   return 1;

} 

