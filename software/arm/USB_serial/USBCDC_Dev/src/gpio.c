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
	 * Init des Sélecteurs d'antenne
	 * Sur les ports P3.25 et P3.26
	 * PINSEL7, bit 19:18 et 21:20
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL7 &= ~(0x3 << 18);
	LPC_PINCON->PINSEL7 &= ~(0x3 << 20);
	//Definir les GPIOs en sortie :
	LPC_GPIO3->FIODIR |= ( 1L << 25);
	LPC_GPIO3->FIODIR |= ( 1L << 26);

	/*
	 * Init des io de la caméra
	 * Sur les ports P2.0, P2.1, P2.2, P2.3 et P2.4
	 * PINSEL4, bit 1:0, 3:2, 5:4, 7:6 et 9:8
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL4 &= ~(0x3 << 0);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 2);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 4);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 6);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 8);
	//Definir les GPIOs en sortie :
	LPC_GPIO2->FIODIR |= ( 1L << 2);
	LPC_GPIO2->FIODIR |= ( 1L << 3);
	//Définir les GPIOS en input
	LPC_GPIO2->FIODIR |= ( 1L << 0);
	LPC_GPIO2->FIODIR |= ( 1L << 1);
	LPC_GPIO2->FIODIR |= ( 1L << 4);
	//Choix des pull-up
	LPC_PINCON->PINMODE4 &= ~( 0x3 << 0);
	LPC_PINCON->PINMODE4 &= ~( 0x3 << 2);
	LPC_PINCON->PINMODE4 &= ~( 0x3 << 8);

	/*
	 * Init des io des resets
	 * Sur les ports P1.31, P2.5, P2.6 et P2.7
	 * PINSEL3, bit 31:30 et PINSEL4, bit 11:10, 13:12 et 15:14
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	LPC_PINCON->PINSEL3 &= ~(0x3 << 30);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 10);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 12);
	LPC_PINCON->PINSEL4 &= ~(0x3 << 14);
	//Definir les GPIOs en sortie :
	LPC_GPIO1->FIODIR |= ( 1L << 31);
	LPC_GPIO2->FIODIR |= ( 1L << 5);
	LPC_GPIO2->FIODIR |= ( 1L << 6);
	LPC_GPIO2->FIODIR |= ( 1L << 7);

	/*
	 * Init des io de controle de l'alimentation
	 * Sur les ports P1.29 P1.24, P1.25, P1.27, P1.26 et P1.28
	 * PINSEL3, bit 27.26, 17:16, 19:18, 23:22, 21:20 et 25:24
	 * Ecrire 00 pour GPIO
	 */
	// Relier les Pin aux GPIOS :
	/*LPC_PINCON->PINSEL3 &= ~(0x3 << 26);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 16);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 18);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 22);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 20);
	LPC_PINCON->PINSEL3 &= ~(0x3 << 24);
	//Definir les GPIOs en sortie :
	LPC_GPIO1->FIODIR |= ( 1L << 29);
	LPC_GPIO1->FIODIR |= ( 1L << 24);
	LPC_GPIO1->FIODIR |= ( 1L << 25);
	LPC_GPIO1->FIODIR |= ( 1L << 27);
	LPC_GPIO1->FIODIR |= ( 1L << 26);
	LPC_GPIO1->FIODIR |= ( 1L << 28);*/
}

int gpio_led1_config(short unsigned int direction, short unsigned int pull)
{
	switch( direction )
	{
		case __GPIO_INPUT__ :
			LPC_GPIO0->FIODIR &= ~( 1L << 23);
			break;
		case __GPIO_OUTPUT__ :
			LPC_GPIO0->FIODIR |= ( 1L << 23);
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -1;
			break;
	}
	switch( pull )
	{
		case __GPIO__PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 14 );
			LPC_PINCON->PINMODE1 |= ( 0x0 << 14 );
			break;
		case __GPIO__PULL_DOWN__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 14 );
			LPC_PINCON->PINMODE1 |= ( 0x3 << 14 );
			break;
		case __GPIO__NO_PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 14 );
			LPC_PINCON->PINMODE1 |= ( 0x2 << 14 );
			break;
		case __GPIO__REPEATER__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 14 );
			LPC_PINCON->PINMODE1 |= ( 0x1 << 14 );
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -2;
			break;
	}
	return 0;
}

int gpio_led2_config(short unsigned int direction, short unsigned int pull)
{
	switch( direction )
	{
		case __GPIO_INPUT__ :
			LPC_GPIO0->FIODIR &= ~( 1L << 24);
			break;
		case __GPIO_OUTPUT__ :
			LPC_GPIO0->FIODIR |= ( 1L << 24);
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -1;
			break;
	}
	switch( pull )
	{
		case __GPIO__PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 16 );
			LPC_PINCON->PINMODE1 |= ( 0x0 << 16 );
			break;
		case __GPIO__PULL_DOWN__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 16 );
			LPC_PINCON->PINMODE1 |= ( 0x3 << 16 );
			break;
		case __GPIO__NO_PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 16 );
			LPC_PINCON->PINMODE1 |= ( 0x2 << 16 );
			break;
		case __GPIO__REPEATER__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 16 );
			LPC_PINCON->PINMODE1 |= ( 0x1 << 16 );
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -2;
			break;
	}
	return 0;
}

int gpio_led3_config(short unsigned int direction, short unsigned int pull)
{
	switch( direction )
	{
		case __GPIO_INPUT__ :
			LPC_GPIO0->FIODIR &= ~( 1L << 25);
			break;
		case __GPIO_OUTPUT__ :
			LPC_GPIO0->FIODIR |= ( 1L << 25);
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -1;
			break;
	}
	switch( pull )
	{
		case __GPIO__PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 18 );
			LPC_PINCON->PINMODE1 |= ( 0x0 << 18 );
			break;
		case __GPIO__PULL_DOWN__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 18 );
			LPC_PINCON->PINMODE1 |= ( 0x3 << 18 );
			break;
		case __GPIO__NO_PULL_UP__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 18 );
			LPC_PINCON->PINMODE1 |= ( 0x2 << 18 );
			break;
		case __GPIO__REPEATER__ :
			LPC_PINCON->PINMODE1 &= ~( 0x3 << 18 );
			LPC_PINCON->PINMODE1 |= ( 0x1 << 18 );
			break;
		case __GPIO_NOTHING__ :
			break;
		default :
			return -2;
			break;
	}
	return 0;
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

void gpio_pico_ant_on()
{
	LPC_GPIO3->FIOSET |= ( 1L << 25 );
}

void gpio_pn_ant_on()
{
	LPC_GPIO3->FIOSET |= ( 1L << 26 );
}

void gpio_pico_ant_off()
{
	LPC_GPIO3->FIOCLR |= ( 1L << 25 );
}

void gpio_pn_ant_off()
{
	LPC_GPIO3->FIOCLR |= ( 1L << 26 );
}

void gpio_reset_ether()
{
	gpio_reset_ether_on();
	delay_delay(10);
	gpio_reset_ether_off();
}

void gpio_reset_pico()
{
	gpio_reset_pico_on();
	delay_delay(10);
	gpio_reset_pico_off();
}

void gpio_reset_lcd()
{
	gpio_reset_lcd_on();
	delay_delay(10);
	gpio_reset_lcd_off();
}

void gpio_reset_pn()
{
	gpio_reset_pn_on();
	delay_delay(10);
	gpio_reset_pn_off();
}

inline void gpio_reset_ether_off()
{
	LPC_GPIO2->FIOCLR |= ( 1L << 7 );
}

inline void gpio_reset_ether_on()
{
	LPC_GPIO2->FIOSET |= ( 1L << 7 );
}

inline void gpio_reset_lcd_off()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 31 );
}

inline void gpio_reset_lcd_on()
{
	LPC_GPIO1->FIOSET |= ( 1L << 31 );
}

inline void gpio_reset_pico_off()
{
	LPC_GPIO2->FIOCLR |= ( 1L << 5 );
}

inline void gpio_reset_pico_on()
{
	LPC_GPIO2->FIOSET |= ( 1L << 5 );
}

inline void gpio_reset_pn_off()
{
	LPC_GPIO2->FIOCLR |= ( 1L << 6 );
}

inline void gpio_reset_pn_on()
{
	LPC_GPIO2->FIOSET |= ( 1L << 6 );
}
void gpio_alim_pn_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 24 );
}

void gpio_alim_cam_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 27 );
}
void gpio_alim_ecr_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 29 );
}

void gpio_alim_eth_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 28 );
}

void gpio_alim_pico_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 25 );
}

void gpio_alim_spi_on()
{
	LPC_GPIO1->FIOCLR |= ( 1L << 26 );
}

void gpio_alim_cam_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 27 );
}

void gpio_alim_ecr_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 29 );
}

void gpio_alim_eth_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 28 );
}

void gpio_alim_pico_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 25 );
}

void gpio_alim_pn_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 24 );
}

void gpio_alim_spi_off()
{
	LPC_GPIO1->FIOSET |= ( 1L << 26 );
}

void gpio_cam_aim_wake()
{
	gpio_cam_aim_wake_on();
	delay_delay(10);
	gpio_cam_aim_wake_off();
}

void gpio_cam_aim_wake_off()
{
	LPC_GPIO2->FIOCLR |= ( 1L << 2 );
}

void gpio_cam_aim_wake_on()
{
	LPC_GPIO2->FIOSET |= ( 1L << 2 );
}

short unsigned int gpio_cam_good_read()
{
	return (unsigned short)( ( LPC_GPIO2->FIOPIN & ( 1L << 1 ) ) >> 1 );
}

short unsigned int gpio_cam_illu_en()
{
	return (unsigned short)( ( LPC_GPIO2->FIOPIN & ( 1L << 4 ) ) >> 4 );
}

short unsigned int gpio_cam_pwr_down()
{
	return (unsigned short)( ( LPC_GPIO2->FIOPIN & ( 1L << 0 ) ) >> 0 );
}

void gpio_cam_trig()
{
	gpio_cam_trig_on();
	delay_delay(10);
	gpio_cam_trig_off();
}

void gpio_cam_trig_off()
{
	LPC_GPIO2->FIOCLR |= ( 1L << 3 );
}

void gpio_cam_trig_on()
{
	LPC_GPIO2->FIOSET |= ( 1L << 3 );
}

void gpio_cam_trig_output()
{
		LPC_GPIO2->FIODIR |= ( 1L << 3);
}

void gpio_cam_trig_input()
{
		LPC_GPIO2->FIODIR &= ~( 1L << 3);
		//Choix des pull-up
		LPC_PINCON->PINMODE4 &= ~( 0x3 << 6);
}
