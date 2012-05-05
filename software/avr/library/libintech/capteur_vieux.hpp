#ifndef CAPTEUR_VIEUX_HPP
#define CAPTEUR_VIEUX_HPP
#include <stdint.h>
#include <avr/io.h>
#include "algorithm.hpp"
#include <libintech/timer.hpp>
#include <util/delay.h>

/** @file libintech/capteur_vieux.hpp
 *  @brief Ce fichier crée une classe capteur_srf05 pour pouvoir utiliser simplement les capteurs SRF05.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

/** Fonctions de lecture et écriture de bits. */
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


// typedef Timer<1,ModeCounter,256> timerCapteur;
typedef Serial<0> serial_t_;

/** @class capteur_srf05
 *  \brief Classe pour pouvoir gérer facilement les capteurs srf05.
 *  La classe gère la récupération d'une distance entre le capteur et un obstacle.
 */

template< class Timer >
class capteur_srf05
{
   private:
    static const uint8_t port = PORTD6;
    static volatile bool busy;
    
   public:
    /** S'occupe d'initialiser le capteur.
     */
    static void init()
    {
        // Initialisation du timer. C'est tout.
        Timer::init();
        busy = false;
    }
    
    /** Envoie une impulsion dans la pin, puis active les interruptions de changement
     *  d'état sur cette pin.
     */
    static void value()
    {
        // Si on n'est pas busy (càd si on n'est pas en train d'attendre
        // l'impulsion retour du capteur).
        if (not busy)
        {      
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
            
            // On est busy en attendant l'interruption.
            busy = true;
        }

    }
  
    /** Fonction appellée par l'interruption. S'occupe d'envoyer la valeur de la longueur
     *  de l'impulsion retournée par le capteur dans la série.
     */
    static void interruption()
    {
        // Front montant si bit == 1, descendant sinon.
        uint8_t bit = rbi(PIND, PORTD6);
        
        // Début de l'impulsion
        if (bit)
        {
            // Initialisation du capteur.
            Timer::value(0);
        }
            
        // Fin de l'impulsion
        else// if (!bit && flag != 1)
        {
            serial_t_::print(Timer::value()*500/184);
            busy = false;
            // Désactivation des interruptions
            cbi(PCICR,PCIE2);
            cbi(PCMSK2,PCINT22);
            
        }


    }

  
};

#endif