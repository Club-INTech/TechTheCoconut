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

int gpio_led1_config(short unsigned int direction, short unsigned int pull);
int gpio_led2_config(short unsigned int direction, short unsigned int pull);
int gpio_led3_config(short unsigned int direction, short unsigned int pull);

void gpio_led1_on();
void gpio_led2_on();
void gpio_led3_on();

void gpio_led1_off();
void gpio_led2_off();
void gpio_led3_off();

void gpio_pico_ant_on();
void gpio_pn_ant_on();

void gpio_pico_ant_off();
void gpio_pn_ant_off();

void gpio_reset_lcd();
void gpio_reset_pico();
void gpio_reset_pn();
void gpio_reset_ether();

inline void gpio_reset_lcd_on();
inline void gpio_reset_ether_on();
inline void gpio_reset_pn_on();
inline void gpio_reset_pico_on();

inline void gpio_reset_lcd_off();
inline void gpio_reset_ether_off();
inline void gpio_reset_pn_off();
inline void gpio_reset_pico_off();

void gpio_alim_ecr_on();
void gpio_alim_pn_on();
void gpio_alim_pico_on();
void gpio_alim_cam_on();
void gpio_alim_spi_on();
void gpio_alim_eth_on();

void gpio_alim_ecr_off();
void gpio_alim_pn_off();
void gpio_alim_pico_off();
void gpio_alim_cam_off();
void gpio_alim_spi_off();
void gpio_alim_eth_off();

void gpio_cam_aim_wake_on();
void gpio_cam_aim_wake_off();
void gpio_cam_aim_wake();

void gpio_cam_trig_on();
void gpio_cam_trig_off();
void gpio_cam_trig();

unsigned short gpio_cam_pwr_down();
unsigned short gpio_cam_good_read();
unsigned short gpio_cam_illu_en();

void gpio_cam_trig_output();
void gpio_cam_trig_input();


#endif /* GPIO_H_ */
