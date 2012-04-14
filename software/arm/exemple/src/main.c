//#include "mbed.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "LPC17xx.h"

//TEMPS est le temps que l'on va attendre avant de faire l'instruction suivante (wait(TEMPS))
#define TEMPS 1000

#define F_CPU 100000000

//Definition des numéros de pin de sortie des LEDs
#define LED1 22

//#define ON

//Définition du port de configuration et du port de sortie pour les LEDs
#define PORT_CONFIG LPC_GPIO0->FIODIR
#define PORT_SORTIE LPC_GPIO0->FIOPIN

volatile uint32_t msTicks;                            /* counts 1ms timeTicks */
/*----------------------------------------------------------------------------
  SysTick_Handler
 *----------------------------------------------------------------------------*/
void SysTick_Handler(void) {
  msTicks++;                        /* increment counter necessary in Delay() */
}

/*------------------------------------------------------------------------------
  delays number of tick Systicks (happens every 1 ms)
 *------------------------------------------------------------------------------*/
__INLINE static void Delay (uint32_t dlyTicks) {
  uint32_t curTicks;

  curTicks = msTicks;
  while ((msTicks - curTicks) < dlyTicks);
}

//Début du programme principal
int main()
{

	if (SysTick_Config(SystemCoreClock / 1000))
	{ /* Setup SysTick Timer for 1 msec interrupts  */
    		while (1);                                  /* Capture error */
	}


    //Configuration du port en sortie pour les LEDs et remise à zéro des sorties
	PORT_CONFIG |= 0x00400000;
	PORT_SORTIE &= ~0x00400000;
#ifndef ON
        PORT_SORTIE &= ~(1 << LED1);            //Mise à 0 de la LED1
#endif
#ifdef ON
        PORT_SORTIE |= (1 << LED1);             //Mise à 1 de la LED1
#endif
	return 0;
}


