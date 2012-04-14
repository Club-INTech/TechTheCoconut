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
#include "delay.h"

void gpio_init()
{
	/*
	 * Init des LED de debug
	 * Sur les port P0.23, P0.24 et P0.25
	 * PINSEL1, bit 15:14, 17:16 et 19:18
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL1 &= ~(0x3 << 14);
	LPC_PINCON->PINSEL1 &= ~(0x3 << 16);
	LPC_PINCON->PINSEL1 &= ~(0x3 << 18);
	//Definir les GPIOs en sortie :
	LPC_GPIO0->FIODIR |= ( 1L << 23);
	LPC_GPIO0->FIODIR |= ( 1L << 24);
	LPC_GPIO0->FIODIR |= ( 1L << 25);

	/*
	 * Init des io de la caméra
	 * Sur les ports P2.0, P2.1, P2.2, P2.3 et P2.4
	 * PINSEL4, bit 1:0, 3:2, 5:4, 7:6 et 9:8
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL4 &= ~(0x3 << 2);
	//Définir les GPIOS en input
	LPC_GPIO2->FIODIR |= ( 1L << 1);
	//Choix des pull-up
	LPC_PINCON->PINMODE4 &= ~( 0x3 << 2);
}

void gpio_led1_on()
{
	LPC_GPIO0->FIOSET |= ( 1L << 23 );
}

void gpio_led2_on()
{
	LPC_GPIO0->FIOSET |= ( 1L << 24 );
}
void gpio_led3_on()
{
	LPC_GPIO0->FIOSET |= ( 1L << 25 );
}

void gpio_led1_off()
{
	LPC_GPIO0->FIOCLR |= ( 1L << 23 );
}

void gpio_led2_off()
{
	LPC_GPIO0->FIOCLR |= ( 1L << 24 );
}

void gpio_led3_off()
{
	LPC_GPIO0->FIOCLR |= ( 1L << 25 );
}

short unsigned int gpio_read()
{
	return (unsigned short)( ( LPC_GPIO2->FIOPIN & ( 1L << 1 ) ) >> 1 );
}
