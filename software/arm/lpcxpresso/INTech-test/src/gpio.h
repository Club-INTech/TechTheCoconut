/*
 * gpio.h
 *
 *  Created on: 30 nov. 2011
 *      Author: jeremy
 */
#ifndef GPIO_H_
#define GPIO_H_

#define __GPIO__PULL_UP__ 1
#define __GPIO__PULL_DOWN__ 2
#define __GPIO__NO_PULL_UP__ 3
#define __GPIO__REPEATER__ 4

#define __GPIO_NOTHING__ 0
#define __GPIO_OUTPUT__ 1
#define __GPIO_INPUT__ 2

void gpio_init();

void gpio_led1_on();
void gpio_led2_on();
void gpio_led3_on();
void gpio_led1_off();
void gpio_led2_off();
void gpio_led3_off();

unsigned short gpio_read();

#endif /* GPIO_H_ */
