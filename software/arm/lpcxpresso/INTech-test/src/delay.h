/*
 * delay.h
 *
 *  Created on: 30 nov. 2011
 *      Author: jeremy
 */

#ifndef DELAY_H_
#define DELAY_H_


void SysTick_Handler (void);

void delay_delay( unsigned long interval );

void delay_init();

unsigned long delay_time();

#endif /* DELAY_H_ */
