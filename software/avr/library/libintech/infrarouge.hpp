#ifndef INFRAROUGE_HPP
#define INFRAROUGE_HPP
#include <stdint.h>
#include <avr/io.h>
#include "algorithm.hpp"


class infrarouge{
private:
  static const uint16_t NB_ECHANTILLON =  10;
  static const uint16_t    val_ADCH[NB_ECHANTILLON];
  static const uint16_t    val_mm[NB_ECHANTILLON] ;
  
  static uint16_t indice_tab(uint16_t adch)
  {
      uint16_t i;
      for (i = 1; i < NB_ECHANTILLON -1; i++)
      {
	  if (adch >= val_ADCH[i])
	  {
	      return i-1;
	  }        
      }
      return NB_ECHANTILLON- 2;
  }

   static uint16_t conversion(uint16_t adch)
  {
      uint8_t ind = indice_tab(adch);
      return regression_lin(val_ADCH[ind], val_ADCH[ind+1], val_mm[ind], val_mm[ind+1], adch);        
  }
  
public:
  static void init(){
       ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescalar to 128 - 125KHz sample rate @ 16MHz 

      ADMUX |= (1 << REFS0); // Set ADC reference to AVCC 
      ADMUX |= (1 << ADLAR); // Left adjust ADC result to allow easy 8 bit reading 

      // No MUX values needed to be changed to use ADC0 
	
      ADCSRA |= (1 << 5);  // Set ADC to Free-Running Mode 
      ADCSRA |= (1 << ADEN);  // Enable ADC 
      ADCSRA |= (1 << ADSC);  // Start A2D Conversions 
  }
  
  static uint16_t value(){
  //     if (ADCH <= 15)
  //         return 1500;
      return conversion(ADCH);
  }
  
};

const uint16_t    infrarouge::val_ADCH[NB_ECHANTILLON]   = {170, 150, 120, 100, 80,  50 , 30 , 20 , 10, 0};
const uint16_t    infrarouge::val_mm[NB_ECHANTILLON]     = {50 , 70 , 100, 130, 160, 280, 500, 650, 1500, 1800};

#endif