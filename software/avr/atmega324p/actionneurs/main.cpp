
/** @file avr/atmega324p/actionneurs/main.cpp
 *  @brief Ce fichier s'occupe de gérer l'AVR Capteur-actionneurs
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH :: Série
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

// LIBRAIRIE INTECH :: Capteurs
#include <libintech/ultrason.hpp>
#include <libintech/infrarouge.hpp>
#include <libintech/capteur_srf05.hpp>
#include <libintech/jumper.hpp>

// LIBRAIRIES LOCALES
#include "ax12.h"
#include "actionneurs.h"



/********************************
 *           CONSTANTES         *
 ********************************/

#define BAUD_RATE_SERIE         9600
#define BAUD_RATE_AX12          AX_BAUD_RATE_9600

/******************************** 
 *   MODES DE CONFIGURATION     *   
 ********************************/

// Mode pour reflasher l'id des AX12 connectés. Attention à c'qu'on fait.
// Si ce mode est positif, il reflashera l'id des AX12 à la valeur du mode.
// Pour ne pas reflasher l'id des AX12 connectés, mettre une valeur négative.
    #define FLASH_ID_MODE           -1

// Mode pour reflasher le baud rate d'écoute des AX12. Warning. Achtung.
// Mettre à 0 pour ne pas le reflasher, à 1 sinon. Si ce mode est à 1,
// la carte reflashera le baud rate d'écoute de l'AX12 à la valeur
// BAUD_RATE_AX12 (définie un peu plus haut)
    #define FLASH_BAUD_RATE_MODE    0

// Mode pour tester les AX12 sans utiliser la liaison PC.
// A mettre à 1 pour l'utiliser, à 0 sinon. Si le mode est mis à 1, l'AX12
// tournera en continu.
// WARNING Ce mode fait tourner en rond et en continue les AX12. Donc pensez
//         à les désolidariser du robot avant de lancer ce mode.
    #define TEST_NOSERIE_MODE       0

// Mode si l'AX12 ne répond pas alors qu'il le devrait. Vérifier la masse.
// Si ce mode est utilisé, les diodes de l'AX12 clignotent 5 sec après un
// petit bout de temps (de l'ordre de la minute) et sont alors reset.
// Il faudra reflasher leur baud-rate après (en utilisant le mode ci dessus)
// NOTE : Pour reflasher leur baud-rate, il faudra remettre le baud rate de la
// série de la carte à 1.000.000. (c'est le baud-rate d'écoute 
// Cette solution est dégueux : elle teste tous les baud rate possibles et
// envoie un signal de réset. Si l'AX12 ne répond pas, c'est un problème
// matériel.
    #define REANIMATION_MODE        0

///Fonctions de lecture/écriture de bit (utile pour capteurs & jumper)
// Set Bit
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif

// Clear Bit
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif

// Read Bit
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

/** Ce fichier gère la carte qui fait le lien entre les AX12, les capteurs ultrasons,
 *  le jumper de début de match et la carte PCI.
 * 
 *  La série 1 est dédiée à la communication Carte  ->  AX12
 *  La série 0 est dédiée à la communication Carte <->   PC
 *  Le pin 7 est dédié au jumper.
 *  Le pin analog0 est dédiée aux infrarouges.
 *          Les infrarouges ne sont pas utilisés au démarrage de la carte. Pour les prendre
 *          en compte dans les calculs, envoyer le message "use_infra" à la carte.
 */

// Liaison série
typedef Serial<0> serial_t_;

// Ultrasons
extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;

// Ultrasons SRF05
typedef Timer<1,ModeCounter,256> timerCapteurSRF;
typedef capteur_srf05< timerCapteurSRF, serial_t_ > capteur_srf05_t_;

// Jumper
typedef jumper< AVR_PORTD<PORTD7> > jumper_t_;

/// **************************
/// *     FONCTION MAIN      *
/// **************************
int main()
{
    // Initialisations de tous les objets.
    infrarouge          ::init();
    jumper_t_           ::init();
    capteur_srf05_t_    ::init();
    serial_t_           ::init();
    ultrason_d           .init();
    ultrason_g           .init();
    
    // Changement du BAUD RATE de la série carte <-> AX12
    AX12_Serial_Init(BAUD_RATE_SERIE);

    // Changement du BAUD RATE de la série carte <-> PC
    serial_t_::change_baudrate(BAUD_RATE_SERIE);
    
    if (FLASH_BAUD_RATE_MODE)
        // BAUD RATE de l'AX12 (réception)
        writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
    
    if (FLASH_ID_MODE >= 0)
        AX12InitID(FLASH_ID_MODE);
        
    // Initialisation de tous les AX12 en angle max, angle min et vitesse
    // de rotation
    AX12Init (AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
    
    // Variable utilisée uniquement pour le REANIMATION_MODE :
    byte debug_baudrate = 0x00;
        
    // Activation de toutes les interruptions (notamment les interruptions
    // de la liaison série carte <-> carte.
    sei();
        
    /// BOUCLE PRINCIPALE
    while (1)
    {
        /// Mode de réanimatio, lorsque plus rien d'autre ne marche.
        if (REANIMATION_MODE)
        {
            AX12_Serial_Init(2000000/(debug_baudrate + 1));
            reset(0xFE);
            debug_baudrate++;
        }
        
        /// Test des AX12 sans communiquer avec eux via la liaison série.
        /// Ils sont censés tourner en boucle, donc désolidarisez-les du
        /// robot avant ;)
        else if (TEST_NOSERIE_MODE) 
            AX12Init(0xFE, 0,0,1200);
        
        /// ******************************************
        /// **          PROGRAMME PRINCIPALE        **
        /// ******************************************
        else
        {
            char buffer[17];
            serial_t_::read(buffer,17);
            #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

            // Ping
            if(COMPARE_BUFFER("?", 1)){
                serial_t_::print(3);
            }
            
            // Easter Egg
            else if (COMPARE_BUFFER("s", 1))
            {
                serial_t_::print("SOPAL'INT\n\r-------\n\n\rSopal'INT VA VOUS METTRE\n\r\
                                    LA RACE !!!!\n\r***********");
            }

            // GoTo angle
            else if (COMPARE_BUFFER("GOTO", 4))
            {
                int8_t id = serial_t_::read_int();
                int16_t angle = serial_t_::read_int();

                AX12GoTo(id, AX_ANGLECW + (int16_t)(600.*angle/180.));
            }
            
            // Goto Broadcast
            else if (COMPARE_BUFFER("g", 1))
            {
                int8_t angle = serial_t_::read_int();
                
                AX12GoTo(0xFE, AX_ANGLECW + (int16_t)(600.*angle/180.));
            }
        
            // Changement de vitesse
            else if (COMPARE_BUFFER("CH_VITESSE", 10))
            {
                int16_t speed = serial_t_::read_int();
                AX12ChangeSpeed(0xFE, speed);
            }
            
            // Reflashage de tous les servos branchés
            else if (COMPARE_BUFFER("FLASH_ID", 8))
            {
                int8_t id = serial_t_::read_int();
                AX12InitID(id);
            }
            
            // Désasservissement de tous les servos branchés
            else if (COMPARE_BUFFER("UNASSERV", 8))
                AX12Unasserv(0xFE);
            

            
            /// *********************************************** ///
            ///                 CAPTEURS                        ///
            /// *********************************************** ///
            
            // Jumper
            else if (COMPARE_BUFFER("jumper", 6))
                serial_t_::print(jumper_t_::value());
            
            // ultrasons
            else if (COMPARE_BUFFER("ultrason", 8))
                serial_t_::print(max(ultrason_g.value(),ultrason_d.value()));
            
            // infrarouge
            else if (COMPARE_BUFFER("infra", 5))
                serial_t_::print(infrarouge::value());
            
            // Ultrasons SRF05
            else if (COMPARE_BUFFER("SRF", 3))
                capteur_srf05_t_::value();
                
        }
    }
    return 0;
}


// Overflow du timer 1
ISR(TIMER1_OVF_vect){
    
}
