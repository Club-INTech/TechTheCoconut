#ifndef CAPTEUR_SRF05_HPP
#define CAPTEUR_SRF05_HPP

// Librairie standard :
#include <stdint.h>
#include <avr/io.h>
#include <util/delay.h>

// Librairie INTech :: Timer
#include <libintech/timer.hpp>

// Librairie INTech spéciale série
#include <libintech/serial/serial_0.hpp>


/** @file libintech/capteur_srf05.hpp
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

/** @class capteur_srf05
 *  \brief Classe pour pouvoir gérer facilement les capteurs srf05.
 * 
 *  \param Timer    L'instance de Timer utilisé pour le calcul de distance.
 *  \param Serial   L'instance de Série utilisée pour communiquer le résultat.
 * 
 *  La classe gère la récupération d'une distance entre le capteur et un obstacle.
 *  
 *  Protocole de ces capteurs :
 *  ---------------------------
 *
 *  La carte envoie une impulsion sur la pin pendant une durée de ~10µs. Puis, après
 *  une durée inconnue, le capteur envoie une impulsion sur cette même pin. La durée
 *  de cette impulsion est proportionnelle à la distance entre les capteurs et l'objet
 *  détecté.  
 */

template< class Timer , class Serial>
class capteur_srf05
{
   private:
    static const uint8_t port = PORTC2;
    static volatile bool busy;
    
   public:
    /** S'occupe d'initialiser le capteur.
     */
    static void init()
    {
        // Initialisation du timer. C'est tout.
        Timer::init();
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
            // Désactivation des interruptions
            cbi(PCICR,PCIE2);
            cbi(PCMSK2,PCINT18);
            
            // Port "port" en output
            sbi(DDRC, port);
            
            // On met un zéro sur la pin pour 2 µs
            cbi(PORTC, port);
            _delay_us(2);
            
            // On met un "un" sur la pin pour 5 µs
            sbi(PORTC, port);
            _delay_us(10);
            
            // On remet un zéro puis on la met en input
            cbi(PORTC, port);
            cbi(DDRC, port);

            // On lance l'interruption qui gèrera la sortie du capteur
            sbi(PCMSK2,PCINT18); // PCINT18 pour PORTC2
            sbi(PCICR,PCIE2);//active PCINT
            sei();
            
            Timer::value(0);
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
        uint8_t bit = rbi(PINC, port);
        // Début de l'impulsion
        if (bit)
        {
            // Réinitialisation du capteur.
            Timer::value(0);
        }
            
        // Fin de l'impulsion
        else
        {
            // Si le timerOverflow n'a pas été lancé. sdfmodsfkgmodsj
            if (busy)
                /// Envoi de la valeur mesurée sur la série. 
                Serial::print(Timer::value()*1050/1800.);
            
            // On n'est plus busy et on peut recevoir un nouvel ordre.
            busy = false;
            
            // Désactivation des interruptions
            cbi(PCICR,PCIE2);
            cbi(PCMSK2,PCINT18);
        }
    }
    
    /// Overflow du timer.
    static void timerOverflow()
    {
        // Trame d'overflow
        if (busy == true)
        {
            Serial::print("noresponse");
        }
        

        // Désactivation des interruptions
        else{
        cbi(PCICR,PCIE2);
        cbi(PCMSK2,PCINT18);
        }
        busy = false;
        

    }
};

#endif