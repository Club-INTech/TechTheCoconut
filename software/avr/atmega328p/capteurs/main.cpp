#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

#include <stdint.h>
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <libintech/timer.hpp>
#include <libintech/capteur_max.hpp>

//Fonctions de lecture/écriture de bit
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;

typedef Serial<0> serial_t_;

int main() {
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    
    ultrason_d.init();
    ultrason_g.init();
    
    while(1) 
    { 
        char buffer[17];
        serial_t_::read(buffer,17);

        #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

        if(COMPARE_BUFFER("?",1)){
            serial_t_::print(1);
        }
        
        if(COMPARE_BUFFER("ultrason",8)){
            serial_t_::print(max(ultrason_g.value(),ultrason_d.value()));
        }

        if(COMPARE_BUFFER("jumper",6)){
            serial_t_::print(rbi(PIND,PD7));
        }
    }

    
}

ISR(TIMER1_OVF_vect){
    
}


