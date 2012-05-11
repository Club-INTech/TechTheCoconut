#ifndef _WATCHDOG_H_
#define _WATCHDOG_H_

#include <avr/wdt.h>
#include <avr/interrupt.h>

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

bool WDT_is_reset();
void WDT_off(void);
void WDT_on(void);
void WDT_set_prescaler(void);

#endif
