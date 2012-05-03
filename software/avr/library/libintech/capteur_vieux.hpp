#ifndef CAPTEUR_VIEUX_HPP
#define CAPTEUR_VIEUX_HPP
#include <stdint.h>
#include <avr/io.h>
#include "algorithm.hpp"
#include <libintech/timer.hpp>

// Set bit
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif
// Clear bit
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif
// Read bit
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif


typedef Timer<1,ModeCounter,64> timerCapteur;
typedef Serial<0> serial_t_;

uint8_t CAPTEUR_VIEUX_BUSY = 0;
uint8_t craineau = 0;


class capteur_vieux{
private:
    static const uint8_t        port                        = PORTD6;
    static const uint16_t       TIMEOUT                     = 1500;
    
    
    static const uint8_t        pin_capteur_vieux           = (1 << port);

  
  static uint32_t ping()
  {
        static const uint8_t pin = pin_capteur_vieux;
        
        // Envoi d'une impulsion dans le capteur
        DDRC |= pin;
        PORTC &= ~pin;
        _delay_us(2);
        PORTC |= pin;
        _delay_us(5);
        PORTC &= ~pin;
        // Reception de la duree
        DDRC &= ~pin;

        uint8_t masque = pin;
        uint32_t duree = 0;
        uint16_t duree_max = TIMEOUT;
        
        // Attente de la fin de l'impulsion precedente
        while ((PINC & pin) == masque)
            if (duree++ == duree_max)
                return 0;
            
        // Attente du demarrage de l'impulsion
        while ((PINC & pin) != masque)
            if (duree++ == duree_max)
                return 0; 
            
        // Attente de la fin de l'impulsion
        while ((PINC & pin) == masque)
                duree++;
        
        return duree;
  }
  


  
public:
  static void init()
  {
      timerCapteur::init();
//       sbi(DDRD, PORTD5);
  }
  
  static uint16_t value()
  {
      return ping();
  }
  
  static void test()
  {
      // Si on n'est pas busy busy
      if (!CAPTEUR_VIEUX_BUSY)
      {
        serial_t_::print("TEST");
        CAPTEUR_VIEUX_BUSY = 1;
        
        
        // Port "port" en output
        sbi(DDRD, port);
        
        // On met un zéro sur la pin pour 2 µs
        cbi(PORTD, port);
        _delay_us(2);
        
        // On met un "un" sur la pin pour 5 µs
        sbi(PORTD, port);
        _delay_us(5);
        
        // On remet un zéro puis on la met en input
        cbi(PORTD, port);
        cbi(DDRD, port);

        // On lance l'interruption qui gèrera la sortie du capteur
        sbi(PCMSK2,PCINT22); // WARNING PCINT22 est SPECIAL POUR LE PORT PD6 TODO TODO A CHANGER POUR
                            // PORTER LE CODE SUR LA CARTE (mettre PCINT16 pour PortC0)
        sbi(PCICR,PCIE2);//active PCINT port D
        sei(); // Activation de toutes les interruptions
      }
  }
  
  
  static void test2()
  {
      serial_t_::print("test2");
        if (craineau)
            sbi(DDRD, PORTD5);
        else
            cbi(DDRD, PORTD5);
        craineau =  1 - craineau;
        _delay_us(500000);
  }
  
};

ISR(PCINT2_vect)
{
//     changedbits = PIND ^ portchistory;
//     portchistory = PIND;
//     serial_t_::print("ISR");
//     // Début de l'impulsion
//     if (rbi(PIND, PORTD6))
//     {
//         serial_t_::print("ISR_MONTANT");
//         timerCapteur::value(0);
//     }
//     
//     // Fin de l'impulsion
//     else
//     {
//         serial_t_::print("ISR_DESCENDANT");
//         serial_t_::print(timerCapteur::value());
//         CAPTEUR_VIEUX_BUSY = 0;
//     }
    
    
}

#endif