#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "LPC17xx.h"
#include "blink.h"


#define LED 22


#define PORT_CONFIG LPC_GPIO0->FIODIR
#define PORT_SORTIE LPC_GPIO0->FIOPIN

int main()
{
	portConfig( LED, 1);
	ledOff( LED );
	return 0;
}
