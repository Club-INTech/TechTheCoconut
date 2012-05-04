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


typedef Timer<1,ModeCounter,256> timerCapteur;
typedef Serial<0> serial_t_;

class capteur_vieux{
private:
    static const uint8_t        port            = PORTD6;
    static const uint16_t       TIMEOUT         = 1500;
    static volatile bool busy;
    
public:
  static void init()
  {
      timerCapteur::init();
      
      // La pin D5 est là pour génerer un craîneau (optionel)
      sbi(DDRD, PORTD5);
  }
  
  static void test()
  {
//       serial_t_::print(flag);
      // Si on n'est pas busy busy
      if (not busy)
      {
//         serial_t_::print("TEST");
        
        
        // Port "port" en output
        sbi(DDRD, port);
        
        // On met un zéro sur la pin pour 2 µs
        cbi(PORTD, port);
        _delay_us(2);
        
        // On met un "un" sur la pin pour 5 µs
        sbi(PORTD, port);
        _delay_us(10);
        
        // On remet un zéro puis on la met en input
        cbi(PORTD, port);
        cbi(DDRD, port);

        // On lance l'interruption qui gèrera la sortie du capteur
        sbi(PCMSK2,PCINT22); // WARNING PCINT22 est SPECIAL POUR LE PORT PD6 TODO TODO A CHANGER POUR
                            // PORTER LE CODE SUR LA CARTE (mettre PCINT16 pour PortC0)
        sbi(PCICR,PCIE2);//active PCINT port D
        sei();
        
        busy = true;
      }

  }
  
    // Fonction appellée par l'interruption
    static void interruption()
    {
            uint8_t bit = rbi(PIND, PORTD6);
            
            // Début de l'impulsion
            if (bit)
            {
                timerCapteur::value(0);
            }
                
            // Fin de l'impulsion
            else// if (!bit && flag != 1)
            {
                serial_t_::print(timerCapteur::value());
                busy = false;
                // Désactivation des interruptions
                cbi(PCICR,PCIE2);
                cbi(PCMSK2,PCINT22);
                
            }


    }

  
};

volatile bool capteur_vieux::busy = false;


// Interruption pour un changement d'état sur la pin.
ISR(PCINT2_vect)
{
    capteur_vieux::interruption();
}


#endif