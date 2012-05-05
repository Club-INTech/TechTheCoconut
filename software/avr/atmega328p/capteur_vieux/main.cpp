// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/capteur_srf05.hpp>
#include <libintech/timer.hpp>

typedef Serial<0> serial_t_;
typedef Timer<1,ModeCounter,256> timerCapteur;
typedef capteur_srf05< timerCapteur, serial_t_ > capteur_srf05_t_;

int main()
{
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    capteur_srf05_t_::init();
    
    while(1) 
    {
            capteur_srf05_t_::value();
            _delay_ms(100);
    }

    
    return 0;
}

// Interruption pour le timer1
ISR(TIMER1_OVF_vect)
{
    
}

