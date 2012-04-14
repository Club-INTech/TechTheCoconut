#include <stdio.h>
#include <stdlib.h>
#include "blink.h"
#include "LPC17xx.h"

void portConfig( unsigned long pin, unsigned short etat)
{
	if( etat != 0 )
		LPC_GPIO0->FIODIR |= ( 1L << pin );
	else
		LPC_GPIO0->FIODIR &= ( 1L << pin );
}

void ledOn( unsigned long pin)
{
	LPC_GPIO0->FIOPIN |= ( 1L << pin );
}

void ledOff( unsigned long pin)
{
	LPC_GPIO0->FIOPIN &= ~( 1L << pin );
}
