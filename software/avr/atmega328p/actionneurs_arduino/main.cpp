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
// tournera en continu.
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
    ax12Init(BAUD_RATE_SERIE);
    
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
            ax12Init(2000000/(debug_baudrate + 1));
            reset(0xFE);
            debug_baudrate++;
        }
        
        else if (TEST_NOSERIE_MODE) 
            AX12Init(0xFE, 0,0,1200);
        
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
        
            // Changement de vitesse
            else if (COMPARE_BUFFER("CH_VITESSE", 10))
            {
                int16_t speed = serial_t_::read_int();
                AX12Init(AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW , speed);
            }
            
            // Désasservissement de tous les servos branchés
            else if (COMPARE_BUFFER("UNASSERV", 8))
                AX12Unasserv(0xFE);
            
            // Reflashage de tous les servos branchés
            else if (COMPARE_BUFFER("FLASH_ID", 8))
            {
                int8_t id = serial_t_::read_int();
                AX12InitID(id);
            }
            
        }
    }
    return 0;
}


