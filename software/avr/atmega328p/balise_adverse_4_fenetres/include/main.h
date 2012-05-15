#ifndef _MAIN_H_
#define _MAIN_H_

#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <avr/io.h>
#include <stdint.h>  
#include <avr/interrupt.h>
#include "timeToDistance.h"
#include "crc8.h"

#define TIME_THRESHOLD_MIN 100

#ifndef sbi
#define sbi(port,bit) (port) |= (1 << (bit))
#endif

#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif

#ifndef tbi
#define tbi(port,bit) (port) ^= (1 << (bit))
#endif

#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

void setup();

#endif

