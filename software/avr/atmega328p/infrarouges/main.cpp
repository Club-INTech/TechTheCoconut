// LIBRAIRIES STANDARD
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// LIBRAIRIE INTECH
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/capteur_infrarouge.hpp>

//Fonctions de lecture/écriture de bit (utile pour capteurs & jumper)
#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif
#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif


typedef Serial<0> serial_t_;

int main (void) 
{ 
    serial_t_::init();
    serial_t_::change_baudrate(9600);
    capteur_infrarouge::init();
    
   while (1)  // Loop Forever 
   {
        char buffer[17];
        serial_t_::read(buffer,17);
        #define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
        
        // ping
        if (COMPARE_BUFFER("?", 1))
            serial_t_::print(5);
            
        if(COMPARE_BUFFER("infra", 5)){
            serial_t_::print(capteur_infrarouge::value());
        }
        
        

   }    
   
   return 1;

} 

