#include <util/delay.h>
#include "ax12.h"
#include "actionneurs.h"
#include <util/delay.h>

#define current_id 5
#define FLASH_ID_MODE
// #define DEBUG_MODE
#define REANIMATION_MODE



int main()
{
    byte debug_baudrate = 0xFF;
    byte reanimation_compteur = 0x00;
    while (1)
    {
        #ifdef DEBUG_MODE
            if (debug_baudrate >= 0xF9)
                ax12Init(1000000);
            else
                ax12Init(200000);
        
            debug_baudrate+=4;
            
        #elif defined(REANIMATION_MODE)
            
            if (reanimation_compteur < 0x10)
            {
                debug_baudrate--;
                reanimation_compteur += 10;
            }
            ax12Init(2000000/(debug_baudrate+1));
            reset(0xFE);
            reanimation_compteur += 4;
            
        
            
        #else
            ax12Init(8000);
        #endif
            
            
            
        writeData (0xFE, AX_BAUD_RATE, 1, 0x09);
        
        #ifdef FLASH_ID_MODE
            AX12InitID(current_id);
        #endif
            
        AX12Init (0xfE, 0, 0,500);
        AX12GoTo(0xfe, 0);
    }
    return 0;
}