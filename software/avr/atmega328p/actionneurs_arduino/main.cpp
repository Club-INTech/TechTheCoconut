// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

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
// ira à un angle de 90°
    #define TEST_NOSERIE_MODE       0

// Mode si l'AX12 ne répond pas alors qu'il le devrait. Vérifier la masse.
// Si ce mode est utilisé, les diodes de l'AX12 clignotent 5 sec après un
// petit bout de temps (de l'ordre de la minute) et sont alors reset.
// Il faudra reflasher leur baud-rate après (en utilisant le mode ci dessus)
// NOTE : Pour reflasher leur baud-rate, il faudra remettre le baud rate de la
// série de la carte à 1.000.000. (c'est le baud-rate d'écoute 
// Cette solution est dégueux : elle teste tous les baud rate possibles et
// envoie un signal de réset. Si l'AX12 ne répond pas, c'est un problème
// matériel. Vérifier la masse, puis faire revérifier la masse par un 2A
    #define REANIMATION_MODE        0


/**     Ce fichier permet de flasher un arduilol pour pouvoir reprendre le contrôle
 *      en cas de pépin (le bref).
 */
typedef Serial<0> serial_t_;

int main()
{
    // Initialisation de la liaison série PC <-> Carte.
    serial_t_::init();
    serial_t_::change_baudrate(BAUD_RATE_SERIE);
    
    // REANIMATION_MODE :
    byte debug_baudrate = 0x00;
        
    // BAUD RATE de la série (envoi)
    AX12_Serial_Init(BAUD_RATE_SERIE);
    
    if (FLASH_BAUD_RATE_MODE)
        // BAUD RATE de l'AX12 (réception)
        writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
    
    if (FLASH_ID_MODE >= 0)
        AX12InitID(FLASH_ID_MODE);
        
    // Initialisation de tous les AX12
    AX12Init (AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
    
    
        
    while (1)
        
    {
        if (REANIMATION_MODE)
        {
            AX12_Serial_Init(2000000/(debug_baudrate + 1));
            reset(0xFE);
            debug_baudrate++;
        }
        
        else if (TEST_NOSERIE_MODE) 
        {
            AX12GoTo(0xFE, AX_ANGLECW + (int16_t)(600.*90/180.));
        }
        
        else
        {
            char buffer[17];
            serial_t_::read(buffer,17);
            #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

            // Ping
            if(COMPARE_BUFFER("?", 1))
                serial_t_::print(4);

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
                int16_t angle = serial_t_::read_int();
                
                AX12GoTo(0xFE, AX_ANGLECW + (int16_t)(600.*angle/180.));
            }
            
            // Goto brut
            else if (COMPARE_BUFFER("a", 1))
            {
                int8_t id = serial_t_::read_int();
                int16_t angle = serial_t_::read_int();
                AX12GoTo(id, angle);
            }
            
            else if (COMPARE_BUFFER("z", 1))
            {
                
                AX12GoTo(0xFE, AX_ANGLECW + (int16_t)(600.*80/180.));
                serial_t_::print("z");
            }
            
            else if (COMPARE_BUFFER("e", 1))
            {
                
                AX12GoTo(0xFE, AX_ANGLECW + (int16_t)(600.*100/180.));
                serial_t_::print("e");
            }
            
            // Changement de vitesse
            else if (COMPARE_BUFFER("CH_VIT", 6))
            {
                int8_t  id    = serial_t_::read_int();
                int16_t speed = serial_t_::read_int();
                AX12ChangeSpeed(id, speed);
            }
            
            // Changement de vitesse broadcast
            else if (COMPARE_BUFFER("c", 1))
            {
                int16_t speed = serial_t_::read_int();
                AX12ChangeSpeed(0xFE, speed);
            }
            
            // Changement de l'angleCW (min)
            else if (COMPARE_BUFFER("m", 1))
            {
                int16_t angle = serial_t_::read_int();
                AX12ChangeAngleMIN(0xFE, angle);
            }
            
            else if (COMPARE_BUFFER("M", 1))
            {
                int16_t angle = serial_t_::read_int();
                AX12ChangeAngleMAX(0xFE, angle);
            }
               
            
            // Reflashage de tous les servos branchés
            else if (COMPARE_BUFFER("f", 8))
            {
                int8_t id = serial_t_::read_int();
                AX12InitID(id);
            }
            
            // Désasservissement de tous les servos branchés
            else if (COMPARE_BUFFER("UNASSERV", 8) || COMPARE_BUFFER("u", 1) || COMPARE_BUFFER("", 0))
                AX12Unasserv(0xFE);
            
            else if (COMPARE_BUFFER("U", 1))
            {
                uint8_t id = serial_t_::read_int();
                AX12Unasserv(id);
            }
            
            // Changement de T° MAX.
            else if (COMPARE_BUFFER("t", 1))
            {
                writeData(0xFE, AX_LIMIT_TEMPERATURE, 1, 120);
                writeData(0xFE, AX_UP_LIMIT_VOLTAGE,  1, 180);
                serial_t_::print("ok");
            }

            // LEDs d'alarme.
            else if (COMPARE_BUFFER("LED", 3))
            {
                uint8_t type = serial_t_::read_int();
                
                writeData(0xFE, AX_ALARM_LED, 1, type);
                serial_t_::print("ok");
            }
            
            // Message générique.
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
                
                writeData(id, adresse, n, val);
                
                serial_t_::print("ok");
            }
            
        }
    }
    return 0;
}


