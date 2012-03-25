#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <libintech/timer.hpp>
#include <libintech/serial/serial_0.hpp>
#include <libintech/ring_buffer.hpp>

#include "ax12.h"


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
    
    serial_t_::change_baudrate(57600);
    

    sei();

//     uint8_t id = 0;
    uint8_t masque = 0xFF;
    
    // CES LIGNES BUGGENT
//     AX12Init(0xFE,211, 811, 511);
//     AX12GoTo(0xFE, 500);
    
    // RESET DE L'AX12
    serial_t_::print(0xFF);
    serial_t_::print(0xFF);
    serial_t_::print(0xFE);
    serial_t_::print(0x02);
    serial_t_::print(0x06);            
    serial_t_::print(~(0xfe + 0x02 + 0x06)&masque);
    // INITIALISATION DE LA ROTATION
    
    serial_t_::print(0xFF);
    serial_t_::print(0xFF);
    serial_t_::print(0xFE);
    serial_t_::print(0x03);
    serial_t_::print(24);
    serial_t_::print(0x01);
    serial_t_::print(~(0xfe + 0x03 + 24 + 0x01)&masque);
    
    // ROTATION
    serial_t_::print(0xFF);
    serial_t_::print(0xFF);
    serial_t_::print(0x01);
    serial_t_::print(0x07);
    serial_t_::print(0x03);
    serial_t_::print(0x1E);
    serial_t_::print(0x12);
    serial_t_::print(0x02);
    serial_t_::print(0x00);
    serial_t_::print(0x02);
    serial_t_::print(~(0x01 + 0x07 + 0x03 + 0x1E + 0x12 + 0x02 + 0x00 + 0x02)&masque);
    
    // Action
    serial_t_::print(0xFF);
    serial_t_::print(0xFF);
    serial_t_::print(0xFE);
    serial_t_::print(0x02);
    serial_t_::print(0x05);
    serial_t_::print(0xFA);
    
    
    while (1)
    {

        char buffer[17];
        uint8_t length = serial_t_::read(buffer,17);
        
        #define COMPARE_BUFFER(string) strncmp(buffer, string, length) == 0 && length>0
        
        if (COMPARE_BUFFER("z"))
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
        
        // Réinitialiser l'id de l'AX12 à 1.
        else if (COMPARE_BUFFER("id"))
        {
            serial_t_::print(0xFF);
            serial_t_::print(0xFF);
            serial_t_::print(0xFE);
            serial_t_::print(0x04);
            serial_t_::print(0x03);
            serial_t_::print(0x03);
            serial_t_::print(0x01);
            
            serial_t_::print(~(0xfe + 0x04 + 0x03 + 0x03 + 0x01)&masque);
            
            // 100001001 : 265
            //  11110110
            
        }
        
        // Reset de l'AX12
        else if (COMPARE_BUFFER("reset"))
        {
            serial_t_::print(0xFF);
            serial_t_::print(0xFF);
            serial_t_::print(0xFE);
            serial_t_::print(0x02);
            serial_t_::print(0x06);            
            serial_t_::print(~(0xfe + 0x02 + 0x06)&masque);
            
        } 
        // Tentative de rotation
        else if (COMPARE_BUFFER("r"))
        {
            serial_t_::print(0xFF);
            serial_t_::print(0xFF);
            serial_t_::print(0x01);
            serial_t_::print(0x07);
            serial_t_::print(0x03);
            serial_t_::print(0x1E);
            serial_t_::print(0x55);
            serial_t_::print(0x02);
            serial_t_::print(0x00);
            serial_t_::print(0x02);
            serial_t_::print(~(0x01 + 0x07 + 0x03 + 0x1E + 0x55 + 0x02 + 0x00 + 0x02)&masque);
            
//             id++;
        }
        
        serial_t_::print("HELLO");
        
        // Reset
        
        
            

    }
    
    return 0;
    
    
}


/////////////////////////// BRAS HG //////////////////////////////
ISR(INT0_vect)
{

}




// Le main ne doit pas être répété 300 000 fois
ISR(TIMER1_OVF_vect){
}
