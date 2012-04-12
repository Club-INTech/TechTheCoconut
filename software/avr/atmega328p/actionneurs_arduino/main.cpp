#include <util/delay.h>
#include "ax12.h"
#include "actionneurs.h"

#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>



// #define FLASH_ID_MODE
// #define FLASH_BAUD_RATE_MODE
// #define TEST_NOSERIE_MODE
// #define REANIMATION_MODE
#define TEST_NOPYTHON_MODE

#include "serial.h"

#include <avr/io.h>
#include <avr/interrupt.h>

typedef Serial<0> serial_t_;

int main()
{
    Serial<0>::init();
    Serial<0>::change_baudrate(9600);
    
    uart_init();
    // REANIMATION_MODE :
    #ifdef REANIMATION_MODE
        byte debug_baudrate = 0x00;
    #endif
        
    // BAUD RATE de la série (envoi)
    ax12Init(BAUD_RATE_SERIE);
    
    #ifdef FLASH_BAUD_RATE_MODE
        // BAUD RATE de l'AX12 (réception)
        writeData(AX_BROADCAST, AX_BAUD_RATE, 1, BAUD_RATE_AX12);
    #endif
        
    #ifdef FLASH_ID_MODE
        AX12InitID(4);
    #endif
        
    // Initialisation de tous les AX12
    AX12Init (AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW, AX_SPEED);
        
    while (1)
    {
        
        #ifdef REANIMATION_MODE
            
            ax12Init(2000000/(debug_baudrate + 1));
            
            debug_baudrate++;
        #endif       
        
        #ifdef TEST_NOSERIE_MODE 
            AX12Init(0x04, 0,0,200);
        #else
            
            
    char buffer[17];
    serial_t_::read(buffer,17);
    #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

        if(COMPARE_BUFFER("?", 1)){
            serial_t_::print(4);
        }

        else if (COMPARE_BUFFER("GOTO", 4))
        {
            #ifdef TEST_NOPYTHON_MODE
                serial_t_::print("GOTO MODE");
            #endif
            int8_t id = serial_t_::read_int();
            int16_t angle = serial_t_::read_int();
            
            serial_t_::print(id);
            serial_t_::print(angle);
            
            AX12GoTo(id, AX_ANGLECW + (int16_t)(600.*angle/180.));
        }
        
        else if (COMPARE_BUFFER("CH_VITESSE", 10))
        {
            #ifdef TEST_NOPYTHON_MODE
                serial_t_::print("CH_VITESSE MODE");
            #endif
            int16_t speed = serial_t_::read_int();

            AX12Init(AX_BROADCAST, AX_ANGLECW, AX_ANGLECCW , speed);
        }
        
        
            

        #endif
// 
    }
    return 0;
}

