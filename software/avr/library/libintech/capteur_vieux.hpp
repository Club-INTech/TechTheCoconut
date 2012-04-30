#ifndef CAPTEUR_VIEUX_HPP
#define CAPTEUR_VIEUX_HPP
#include <stdint.h>
#include <avr/io.h>
#include "algorithm.hpp"


class capteur_vieux{
private:
    static const uint16_t       NB_ECHANTILLON              =  10;  // Nombre de valeurs de la table
    static const uint16_t       val_ADCH[NB_ECHANTILLON]         ;
    static const uint16_t       val_mm[NB_ECHANTILLON]           ;
    static const uint8_t        pin_capteur_vieux           = (1 << PORTC0);
    static const uint16_t       TIMEOUT                     = 1500;
  
   
  // Retourne l'indice i de la table telle que table[i] > adch > table[i+1]  
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
    
   static uint16_t conversion(uint32_t adch)
  {
      uint8_t ind = indice_tab(adch);
      return regression_lin(val_ADCH[ind], val_ADCH[ind+1], val_mm[ind], val_mm[ind+1], adch);        
  }
  
  static uint32_t ping()
  {
        static const uint8_t pin = pin_capteur_vieux;
        
        // Envoi d'une impulsion dans le capteur
        DDRD |= pin;
        PORTD &= ~pin;
        _delay_us(2);
        PORTD |= pin;
        _delay_us(5);
        PORTD &= ~pin;
        // Reception de la duree
        DDRD &= ~pin;

        uint8_t masque = pin;
        uint32_t duree = 0;
        uint16_t duree_max = TIMEOUT;
        
        // Attente de la fin de l'impulsion precedente
        while ((PIND & pin) == masque)
            if (duree++ == duree_max)
                return 0;
        // Attente du demarrage de l'impulsion
        while ((PIND & pin) != masque)
            if (duree++ == duree_max)
                return 0; 
        // Attente de la fin de l'impulsion
        while ((PIND & pin) == masque)
                duree++;
        return duree;
  }
  
public:
  static void init()
  {
       // Rien à faire mais on la laisse quand même.
  }
  
  static uint16_t value()
  {
      return conversion(ping());
  }
  
  static uint32_t value_brut()
  {
      return ping();
  }
  
};

const uint16_t    capteur_vieux::val_ADCH[NB_ECHANTILLON]   = {1800};
const uint16_t    capteur_vieux::val_mm[NB_ECHANTILLON]     = {50 , 70 , 100, 130, 160, 280, 500, 650, 1500, 1800};

#endif