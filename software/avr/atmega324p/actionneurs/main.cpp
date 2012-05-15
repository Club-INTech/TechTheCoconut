
/** @file avr/atmega324p/actionneurs/main.cpp
 *  @brief Ce fichier s'occupe de gérer l'AVR Capteur-actionneurs
 *  @author Thibaut ~MissFrance~
 *  @date 09 mai 2012
 */ 

// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH :: Série
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/serial/serial_1_interrupt.hpp>
#include <libintech/serial/serial_1.hpp>

// LIBRAIRIE INTECH :: Capteurs
#include <libintech/capteur_max.hpp>
#include <libintech/capteur_infrarouge.hpp>
#include <libintech/capteur_srf05.hpp>
#include <libintech/jumper.hpp>
#include <libintech/ax12.hpp>


/********************************
 *           CONSTANTES         *
 ********************************/

#define BAUD_RATE_SERIE         9600

// Angles MIN et MAX en tics (compris entre 0 et 1024, cf. datasheet)
#define AX_ANGLECW              198
#define AX_ANGLECCW             800

// Vitesse de rotation des AX12 (je crois entre 0 et 1024, pas sûr)
#define AX_SPEED                1000

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
    #define NOSERIE_MODE       0

// Mode si l'AX12 ne répond pas alors qu'il le devrait. Vérifier la masse.
// Si ce mode est utilisé, les diodes de l'AX12 clignotent 5 sec après un
// petit bout de temps (de l'ordre de la minute) et sont alors reset.
// Il faudra reflasher leur baud-rate après (en utilisant le mode ci dessus)
// NOTE : Pour reflasher leur baud-rate, il faudra remettre le baud rate de la
// série de la carte à 1.000.000. (c'est le baud-rate d'écoute 
// Cette solution est dégueux : elle teste tous les baud rate possibles et
// envoie un signal de réset. Si l'AX12 ne répond pas, c'est un problème
// matériel.
// NOTE : Il semble que la carte actionneur ne permette pas d'atteindre un tel baudrate
// de 1.000.000. Utiliser un arduilol.
    #define REANIMATION_MODE        0 
    
    
// Baud Rate à flasher sur l'AX12 si le mode FLASH_BAUD_RATE_MODE est mis à 1
#define BAUD_RATE_AX12 (2000000/(BAUD_RATE_SERIE + 1))

/** Ce fichier gère la carte qui fait le lien entre les AX12, les capteurs ultrasons,
 *  le jumper de début de match et la carte PCI.
 * 
 *  La série 1 est dédiée à la communication Carte  ->  AX12
 *  La série 0 est dédiée à la communication Carte <->   PC
 *  Le pin 7 est dédié au jumper.
 *  Le pin analog0 est dédiée aux infrarouges.
 */

// Liaison série Carte <-> PC
typedef Serial<0> serial_t_;
// Liaison série Carte <-> AX12
typedef Serial<1> serial_ax_;

// Système d'AX12
extern AX12<serial_ax_, BAUD_RATE_SERIE> AX;

// Ultrasons MAX
// extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
// extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;

// Ultrasons SRF05
typedef Timer<1,ModeCounter, 64> timerCapteurSRF;
typedef capteur_srf05< timerCapteurSRF, serial_t_ > capteur_srf05_t_;

// Jumper
typedef jumper< AVR_PORTC<PORTC2> > jumper_t_;



/// **************************
/// *     FONCTION MAIN      *
/// **************************
int main()
{
    // Initialisations de tous les objets.
    capteur_infrarouge  ::init();
    jumper_t_           ::init();
    capteur_srf05_t_    ::init();
    serial_t_           ::init();
    serial_ax_          ::init();
//     ultrason_d           .init();
//     ultrason_g           .init();
    
    AX.init(AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
    
    // Changement du BAUD RATE de la série carte <-> PC
    serial_t_::change_baudrate(BAUD_RATE_SERIE);
    // Changement du baud rate de la série carte <-> AX12
//     serial_ax_::change_baudrate(BAUD_RATE_SERIE);
    
    if (FLASH_BAUD_RATE_MODE)
        // BAUD RATE de l'AX12 (réception)
//         writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
        AX.writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
    
    if (FLASH_ID_MODE >= 0)
        AX.initID(0xFE, FLASH_ID_MODE);
        

    // Variable utilisée uniquement pour le REANIMATION_MODE :
    uint8_t debug_baudrate  = 0x00;
    // Variable utilisée uniquement pour le NOSERIE_MODE :
    uint8_t debug_noserie   = 0x00;
        
    // Activation de toutes les interruptions (notamment les interruptions
    // de la liaison série carte <-> carte).
    sei();
    
        
    /// BOUCLE PRINCIPALE
    while (1)
    {
        /// Mode de réanimation, lorsque plus rien d'autre ne marche.
        if (REANIMATION_MODE)
        {
            // On brute-force le baud rate des AX12, et on leur envoie pour chaque baud rate
            // d'écoute un signal de reset.
            while (debug_baudrate < 0xFF)
            {
                serial_ax_::change_baudrate(2000000/(debug_baudrate + 1));
                AX.reset(0xFE);
                debug_baudrate++;
            }
            
            // Une fois que le signal de reset a été reçu, l'AX12 écoute à 1.000.000 bps.
            // Donc à ce baud rate, on reflash le baud rate d'écoute de l'AX12.
            serial_ax_::change_baudrate(1000000);
            AX.writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
            
            // Puis on revient à la valeur initiale, et on lui donne un angle consigne.
            serial_ax_::change_baudrate(BAUD_RATE_SERIE);
            AX.init (AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
            AX.GoTo (AX_BROADCAST, 512);
            
        }
        
        /// Test des AX12 sans communiquer avec eux via la liaison série.
        /// Ils sont censés tourner en boucle, donc désolidarisez-les du
        /// robot avant ;)
        else if (NOSERIE_MODE)
        {
            debug_noserie = 1- debug_noserie;
            AX.GoTo(0xFE, AX_ANGLECW + (uint16_t)(600.*(90-10*debug_noserie)/180.));
            _delay_ms(500);

        }
        
        /// ******************************************
        /// **          PROGRAMME PRINCIPAL         **
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
            else if (COMPARE_BUFFER("sopa", 4))
            {
                serial_t_::print("SOPAL'INT\n\r-------\n\n\rSopal'INT VA VOUS METTRE\n\r\
                                    LA RACE !!!!\n\r***********");
                serial_t_::print("STOP SOPA ! START SOPAL'INT");
            }
            
            // AIDE
            else if (COMPARE_BUFFER("!", 1))
            {
                serial_t_::print("Salut vieux ! Comment vas-tu aujourd'hui ?");
            }
            
            /// *********************************************** ///
            ///                 ACTIONNEURS                     ///
            /// *********************************************** ///
            
            // Initialisation des AX12
            else if (COMPARE_BUFFER("i", 1))
            {
                // Initialisation de tous les AX12 en angle max, angle min et vitesse
                // de rotation
                AX.init (AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
            }
                
            // GoTo angle
            else if (COMPARE_BUFFER("GOTO", 4))
            {
                uint8_t id = serial_t_::read_int();
                uint16_t angle = serial_t_::read_int();

                AX.GoTo(id, AX_ANGLECW + (uint16_t)(600.*angle/180.));
            }
            
            // Goto Broadcast
            else if (COMPARE_BUFFER("g", 1))
            {
                uint16_t angle = serial_t_::read_int();
                
                AX.GoTo(0xFE, AX_ANGLECW + (uint16_t)(600.*angle/180.));
            }
            
            // Goto brut
            else if (COMPARE_BUFFER("a", 1))
            {
                uint8_t id = serial_t_::read_int();
                uint16_t angle = serial_t_::read_int();
                AX.GoTo(id, angle);
            }
            
            // TEST e goto
            else if (COMPARE_BUFFER("z", 1))
            {
                
                AX.GoTo(0xFE, AX_ANGLECW + (uint16_t)(600.*80/180.));
                serial_t_::print("z");
            }
            
            // TEST de goto
            else if (COMPARE_BUFFER("e", 1))
            {
                
                AX.GoTo(0xFE, AX_ANGLECW + (uint16_t)(600.*100/180.));
                serial_t_::print("e");
            }
            
            // Changement de vitesse
            else if (COMPARE_BUFFER("CH_VIT", 6))
            {
                uint8_t  id    = serial_t_::read_int();
                uint16_t speed = serial_t_::read_int();
                AX.changeSpeed(id, speed);
            }
            
            // Changement de vitesse broadcast
            else if (COMPARE_BUFFER("c", 1))
            {
                uint16_t speed = serial_t_::read_int();
                AX.changeSpeed(0xFE, speed);
            }
            
            // Changement de l'angleCW (min)
            else if (COMPARE_BUFFER("m", 1))
            {
                uint16_t angle = serial_t_::read_int();
                AX.changeAngleMIN(0xFE, angle);
            }
            
            // Changement de l'angle CCW (max)
            else if (COMPARE_BUFFER("M", 1))
            {
                uint16_t angle = serial_t_::read_int();
                AX.changeAngleMAX(0xFE, angle);
            }
               
            
            // Reflashage des Ids de tous les servos branchés
            else if (COMPARE_BUFFER("f", 8))
            {
                uint8_t ancien_id = serial_t_::read_int();
                uint8_t nouvel_id = serial_t_::read_int();
                AX.initID(ancien_id, nouvel_id);
            }
            
            // Désasservissement de tous les servos branchés
            else if ((COMPARE_BUFFER("UNASSERV", 8)) || (COMPARE_BUFFER("u", 1)))
                AX.unasserv(0xFE);
            
            
            // Désasservissement d'un servo donné
            else if (COMPARE_BUFFER("U", 1))
            {
                uint8_t id = serial_t_::read_int();
                AX.unasserv(id);
            }
            
            // Changement de T° MAX.
            else if (COMPARE_BUFFER("t", 1))
            {
                AX.writeData(0xFE, AX_LIMIT_TEMPERATURE, 1, 120);
                AX.writeData(0xFE, AX_UP_LIMIT_VOLTAGE,  1, 180);
                serial_t_::print("ok");
            }

            // LEDs d'alarme.
            else if (COMPARE_BUFFER("LED", 3))
            {
                uint8_t type = serial_t_::read_int();
                
                AX.writeData(0xFE, AX_ALARM_LED, 1, type);
            }
            
            // Message générique. Utilisable pour modifier n'importe quoi.
            else if (COMPARE_BUFFER("MESS", 4))
            {
                // On lit l'id
                uint8_t id = serial_t_::read_int();
                
                // On lit l'adresse de début
                uint8_t adresse = serial_t_::read_int();
                
                // On lit le nombre d'octets
                uint8_t n = serial_t_::read_int();
                
                // On lit la valeur à écrire
                uint16_t val = serial_t_::read_int();
                
                AX.writeData(id, adresse, n, val);
                
            }

            
            /// *********************************************** ///
            ///                 CAPTEURS                        ///
            /// *********************************************** ///
            
            // Jumper
            else if (COMPARE_BUFFER(";j", 2))
                serial_t_::print(jumper_t_::value());
            
//             // ultrasons
//             else if (COMPARE_BUFFER(";u", 2))
//                 serial_t_::print(max(ultrason_g.value(),ultrason_d.value()));
            
            // infrarouge
            else if (COMPARE_BUFFER(";i", 2))
                serial_t_::print(capteur_infrarouge::value());
            
            else if (COMPARE_BUFFER(";u", 2))
                serial_t_::print(capteur_infrarouge::value_brut());
            
            // Ultrasons SRF05
            else if (COMPARE_BUFFER(";s", 2))
                capteur_srf05_t_::value();
                                                    // C'est une interruption qui s'occupe d'afficher
                                                    // la valeur.
        }
    }
    return 0;
}


// Overflow du timer 1 (utilisé notamment par les ultrasons SRF05
ISR(TIMER1_OVF_vect){
    capteur_srf05_t_::timerOverflow();
}
