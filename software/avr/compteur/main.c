#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdint.h>

#include <libintech/usart.h>
#include <libintech/twi_slave.h>
#include "compteur.h"


int main( void ){
	
    // Interruptions
    sei();
    
    //Série
    //uart_init();
    
    // I2C
    TWI_Init();

    // Compteur
    compteur_init();
    
    while(1) {
        TWI_Loop();
	//printLong(roue1);
	//printChar(' ');
	//printlnLong(roue2);
    }

    return 0;
    
}
