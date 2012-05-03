// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/capteur_vieux.hpp>

typedef Serial<0> serial_t_;

int main()
{
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    capteur_vieux::init();
    
    while(1) 
    {
//         char buffer[17];
//         serial_t_::read(buffer,17);
//         #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
//         
//         // ping
//         if (COMPARE_BUFFER("?", 1))
//             serial_t_::print(5);
//         
//         if (COMPARE_BUFFER("vieux", 5))
//             serial_t_::print(capteur_vieux::value_brut());

            capteur_vieux::test();

        
    }

    
    return 0;
}


ISR(TIMER1_OVF_vect)
{
    
}

