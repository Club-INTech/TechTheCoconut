#include "watchdog.h"

/**
 * Indique si l'AVR a été reset par le watchdog
 * 
 */
bool WDT_is_reset()
{
	return rbi(MCUSR,WDRF);
}

/**
 * Eteint le watchdog
 * 
 */
void WDT_off(void)
{
	// Désactivation des interruptions
	cli();
	
	/* Clear WDRF in MCUSR */
	MCUSR &= ~(1<<WDRF);
	
	/* Write logical one to WDCE and WDE */
	/* Keep old prescaler setting to prevent unintentional time-out */
	WDTCSR |= (1<<WDCE) | (1<<WDE);
	
	/* Turn off WDT */
	WDTCSR = 0x00;
	
	// Réactivation des interruptions
	sei();
}

/**
 * Active le watchdog
 * 
 */
void WDT_on(void)
{
	sbi(WDTCSR,WDE);
}
 
 
/** 
 * Change le prescaler du watchdog
 * 
 */
void WDT_set_prescaler(void)
{
	// Désactivation des interruptions
	cli();
	
	/* Start timed sequence */
	WDTCSR |= (1<<WDCE) | (1<<WDE);
	
	/* Mise à jour du prescaler */
	WDTCSR = (1<<WDP2);
	
	// Réactivation des interruptions
	sei();
}
