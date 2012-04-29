// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/infrarouge.hpp>
#include "capteurs.h"

typedef Serial<0> serial_t_;

int main()
{
//     // Initialisation I2C
//     TWI_Init();
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    
    volatile uint16_t temp1 = ping(PIN_ULTRASON1);
//     _delay_ms(50);
//     volatile uint16_t temp2 = ping(PIN_ULTRASON2);
    
    while(1) {
        
        _delay_ms(15);
//         if ( temp2 < temp1 )
//             ultrason = temp2;
        temp1 = ping(PIN_ULTRASON1);
        
        serial_t_::print(temp1);
        
//         _delay_ms(15);
//         if ( temp1 < temp2 )
//             ultrason = temp1;
//         temp2 = ping(PIN_ULTRASON2);
//         
//         serial_t_::print(temp2);
    }
    
    return 0;
}

