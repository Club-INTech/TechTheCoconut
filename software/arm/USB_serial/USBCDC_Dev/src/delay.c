/*
 * delay.c
 *
 *  Created on: 30 nov. 2011
 *      Author: jeremy
 */

#include "delay.h"
#include "LPC17xx.h"
#include <string.h>
#include <stdio.h>

volatile unsigned int current_time;

void SysTick_Handler (void)
{
  current_time++;
}

void delay_delay(unsigned int interval)
{
  unsigned int start = current_time;
  while (current_time - start < interval);
}

unsigned long delay_time()
{
	return current_time;
}


void delay_init()
{
#ifdef __V2__
	SysTick_Config (SystemCoreClock / 1000);
#endif
#ifndef __V2__
	SysTick_Config (SystemFrequency / 100);
#endif
}
