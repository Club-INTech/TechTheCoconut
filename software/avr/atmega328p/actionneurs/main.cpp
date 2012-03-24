#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>


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



typedef Timer<1,ModeCounter,8> ClasseTimer;

typedef Serial<0> serial_t_;

ring_buffer<uint16_t, 3> mesures_hg;
ring_buffer<uint16_t, 3> mesures_hd;
ring_buffer<uint16_t, 3> mesures_bg;
ring_buffer<uint16_t, 3> mesures_bd;

uint16_t derniere_valeur_hg;
uint16_t derniere_valeur_hd;
uint16_t derniere_valeur_bg;
uint16_t derniere_valeur_bd;

int compare (const void * a, const void * b)
{
  return ( *(uint16_t*)a - *(uint16_t*)b );
}

int main()
{
    ClasseTimer::init();
    Serial<0>::init();
    
    
    //Pin D4 en OUTPUT
    cbi(DDRB,PORTD4);
    //Activation des interruptions pour tout changement logique pour pin4
    cbi(EICRA,ISC01);
    sbi(EICRA,ISC00);
    sbi(EIMSK,INT0);
    //Activation proprement dite

    sei();

    
    while (1)
    {

        char buffer[17];
        uint8_t length = serial_t_::read(buffer,17);
        #define COMPARE_BUFFER(string) strncmp(buffer, string, length) == 0 && length>0
        
        if (COMPARE_BUFFER("?"))
        {
            serial_t_::print(1);
        }
        
        else if (COMPARE_BUFFER("a"))
        {
            cli();
            qsort(mesures_hd.data(),mesures_hd.size(),sizeof(uint16_t),compare);
            qsort(mesures_hg.data(),mesures_hg.size(),sizeof(uint16_t),compare);
            serial_t_::print(max(mesures_hg.data()[mesures_hg.size()/2],mesures_hd.data()[mesures_hd.size()/2]));
            sei();
        }
        

    }
    
    return 0;
    
}


/////////////////////////// BRAS HG //////////////////////////////
ISR(INT0_vect)
{

    //Front montant
    if(rbi(PIND,PORTD2))
    {
        derniere_valeur_hg = ClasseTimer::value();
    }
    
    // Front descendant
    else
    {
        // prescaler/fcpu*inchToCm/tempsParInch
        if(ClasseTimer::value() <derniere_valeur_hg)
          mesures_hg.append((ClasseTimer::value() + 65536 - derniere_valeur_hg  )*0.0884353741496);
        else
          mesures_hg.append((ClasseTimer::value() - derniere_valeur_hg )*0.0884353741496);
    }
}




// Le main ne doit pas être répété 300 000 fois
ISR(TIMER1_OVF_vect){
}
