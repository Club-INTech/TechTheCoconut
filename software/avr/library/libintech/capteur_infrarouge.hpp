#ifndef INFRAROUGE_HPP
#define INFRAROUGE_HPP
#include <stdint.h>
#include <avr/io.h>
#include "algorithm.hpp"

/** @file libintech/capteur_infrarouge.hpp
 *  @brief Ce fichier crée une classe capteur_infrarouge pour pouvoir utiliser simplement les capteurs SRF05.
 *  @author Thibaut ~MissFrance~
 *  @date 08 mai 2012
 */

class capteur_infrarouge{
private:
  static const uint16_t NB_ECHANTILLON =  8;
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
      return conversion(ADCH);
  }
  
  static uint16_t value_brut()
  {
      return ADCH;
  }
  
};

const uint16_t    capteur_infrarouge::val_ADCH[NB_ECHANTILLON]   = {200, 64, 36, 22, 17, 13, 9, 5};
const uint16_t    capteur_infrarouge::val_mm[NB_ECHANTILLON]     = {70, 100, 200, 300, 400, 500, 600, 900};

#endif