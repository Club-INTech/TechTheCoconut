// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/jumper.hpp>
#include <libintech/register.hpp>

typedef Serial<0> serial_t_;
typedef jumper< AVR_PORTD<PORTD7> > jumper_t_;

int main()
{
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    jumper_t_::init();
    
    while(1) 
    {
            serial_t_::print(jumper_t_::value());
    }

    return 0;
}


