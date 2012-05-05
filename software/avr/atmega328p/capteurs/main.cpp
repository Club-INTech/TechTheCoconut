#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>

#include <stdint.h>
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <libintech/timer.hpp>
#include <libintech/ultrason.hpp>

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
    
    //Pin D2 en INPUT
    cbi(DDRD,DD2);
    //Pin D7 en INPUT
    cbi(DDRD,PD7);
    cbi(PORTD,PD7);//Pull up disabled
    //Activation des interruptions pour tout changement logique pour pin2
    cbi(EICRA,ISC01);
    sbi(EICRA,ISC00);
    sbi(EIMSK,INT0);//Activation proprement dite

    cbi(DDRD,PORTD3);
    //Activation des interruptions pour tout changement logique pour pin3
    cbi(EICRA,ISC11);
    sbi(EICRA,ISC10);
    sbi(EIMSK,INT1);//Activation proprement dite

    sei();
    
    

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


