/*
 * gpio.c
 *
 *  Created on: 30 nov. 2011
 *      Author: jeremy
 */
#include "LPC17xx.h"
#include <string.h>
#include <stdio.h>
#include "gpio.h"

void gpio_init()
{
	/*
	 * Init des LED de debug
	 * Sur les port P4.29
	 * PINSEL9, bit 27:26
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL9 &= ~(0x3 << 26);
	//Definir les GPIOs en sortie :
	LPC_GPIO4->FIODIR |= ( 1L << 29);

}

void gpio_led_reset_on()
{
	LPC_GPIO4->FIOSET |= ( 1L << 29 );
}

void gpio_led_reset_off()
{
	LPC_GPIO4->FIOCLR |= ( 1L << 29 );
}
