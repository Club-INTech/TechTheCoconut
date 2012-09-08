// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

// LIBRAIRIES LOCALES


/********************************
 *           CONSTANTES         *
 ********************************/

#define BAUD_RATE_SERIE         9600

/******************************** 
 *   MODES DE CONFIGURATION     *   
 ********************************/




typedef Serial<0> serial_t_;

int main()
{
    // Initialisation de la liaison série PC <-> Carte.
    serial_t_::init();
    serial_t_::change_baudrate(BAUD_RATE_SERIE);
    
    while (1)
        
    {
       serial_t_::print("1");
       
    }
    return 0;
}


