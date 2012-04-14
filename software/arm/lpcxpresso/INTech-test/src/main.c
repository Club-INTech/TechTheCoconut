/*
===============================================================================
 Name        : main.c
 Author      : $(author)
 Version     :
 Copyright   : $(copyright)
 Description : main definition
===============================================================================
*/

#ifdef __USE_CMSIS
#include "LPC17xx.h"
#endif

#include <cr_section_macros.h>
#include <NXP/crp.h>
#include "gpio.h"
#include "delay.h"
#include <stdio.h>
#include "uart.h"
#include "serial.h"
#include "pwm.h"
#include <cr_section_macros.h>

// Variable to store CRP value in. Will be placed automatically
// by the linker when "Enable Code Read Protect" selected.
// See crp.h header for more information
__CRP const unsigned int CRP_WORD = CRP_NO_CRP ;


#define TEMPS 20
#define TEMPS1 100
#define TEMPS2 30

#define TEMPO 5000

#define UART1 1
#define UART2 2

#define ___DEBUG___


#define CHOIX_TEST 2

#if CHOIX_TEST == 1
	#define ___TEST_PULSE___
#elif CHOIX_TEST == 2
	#define ___TEST_SERIAL___
//	#define ___INTERRUPT___
#elif CHOIX_TEST == 3
	#define ___TEST_PWM___
#else
	#error "Choisir le bon choix de programme"
#endif

#define BUFFER_SIZE 32

#ifdef ___TEST_PWM2___
	extern volatile uint32_t match_counter1;
#endif
#ifdef ___TEST_PULSE___
	extern unsigned char pwm_pulse;
#endif

int state = 0;
int ledState1,ledState2,ledState3 = 1;
int c;

// TODO: insert other definitions and declarations here

/**
 * This will test uart 0 at all the baud rates below to check that error free communication
 * is possible at all the uart baud rates defined in baud_rates.
 *
 * The LPC1768 Uart should be connected to a PC serial port running a terminal emulation
 * program.
 *
 * When the program is started the uart 0 is set to 921600 Bps.
 *
 * With the PC terminal emulation program set to 921600 Bps the user should press a key. The
 * key pressed should then be echo'ed back to the PC by the LPC1768/9 code. This should be
 * repeated for all the baud rates detailed below in baud_rates.
 *
 * This project uses semi hosting for the printf statements. These will be displayed in the IDE.
 */

int main( void )
{
#ifdef ___TEST_SERIAL___
#ifndef ___INTERRUPT___
	initUart(UART1, 9600);
	initUart(UART2, 9600);
	gpio_init();
	delay_init();
	gpio_led1_off();
	gpio_led2_off();
	gpio_led3_off();
	while(42)
	{
		if( UART_isDataAvailable(UART1) )
		{
			c = UART_Getchar(UART1);
			if( ledState3 )
			{
				gpio_led3_on();
				ledState3 = 0;
			}
			else
			{
				gpio_led3_off();
				ledState3 = 1;
			}
			UART_Sendchar(UART1,c);
		}
		if( UART_isDataAvailable(UART2) )
		{
			c = UART_Getchar(UART2);
			if( ledState2 )
			{
				gpio_led2_on();
				ledState2 = 0;
			}
			else
			{
				gpio_led2_off();
				ledState2 = 1;
			}
			UART_Sendchar(UART1,c);
		}
	}
	return 0;
#endif
#ifdef ___INTERRUPT___
	ser_OpenPort(UART1);
	ser_OpenPort(UART2);
	gpio_init();
	gpio_led1_off();
	gpio_led2_on();
	gpio_led3_off();
	int numAvailByte;
	int i;
	while(42)
	{
		ser1_AvailChar(&numAvailByte);
		if( numAvailByte > 0 )
		{
			static char serBuf [BUFFER_SIZE];
			int  numBytesRead;
			numBytesRead = ser0_Read (&serBuf[0], &numAvailByte);
			if( ledState3 )
			{
				gpio_led3_on();
				ledState3 = 0;
			}
			else
			{
				gpio_led3_off();
				ledState3 = 1;
			}
			for( i = 0;i<numBytesRead;++i)
				UART_Sendchar(UART2,serBuf[i]);
		}
		switch( UART2 )
		{
			case 0 :
				ser0_AvailChar(&numAvailByte);
				break;
			case 2 :
				ser2_AvailChar(&numAvailByte);
				break;
			case 3:
				ser3_AvailChar(&numAvailByte);
				break;
		}
		if( numAvailByte > 0 )
		{
			static char serBuf [BUFFER_SIZE];
			int  numBytesRead;
			switch( UART2 )
			{
				case 0 :
					numBytesRead = ser0_Read (&serBuf[0], &numAvailByte);
					break;
				case 2 :
					numBytesRead = ser2_Read (&serBuf[0], &numAvailByte);
					break;
				case 3:
					numBytesRead = ser3_Read (&serBuf[0], &numAvailByte);
					break;
			}
			if( ledState2 )
			{
				gpio_led2_on();
				ledState2 = 0;
			}
			else
			{
				gpio_led2_off();
				ledState2 = 1;
			}
			for( i = 0;i<numBytesRead;++i)
				UART_Sendchar(UART1,serBuf[i]);
		}
	}
	return 0;
#endif
#endif
#ifdef ___TEST_PWM___
	delay_init();
	if ( PWM_Init( ) != 1 )
	{
		while( 1 );			/* fatal error */
	}

	//PWM_Set( CHANNEL_NUM, cycle, offset );

	PWM_Update( ROUGE,  -600 );
	PWM_Update( VERT,  -600 );
	PWM_Update( BLEU,  -600 );
	PWM_Start();
	int i;
	while( 1 )
	{
		for( i=-600;i<600;++i)
		{
			PWM_Update( BLEU, -i);
			PWM_Update( VERT, i);
			delay_delay(TEMPS);
		}
		for( i=-600;i<600;++i)
		{
			PWM_Update( ROUGE, i);
			PWM_Update( VERT, -i);
			delay_delay(TEMPS);
		}
		for( i=-600;i<600;++i)
		{
			PWM_Update( ROUGE, -i);
			PWM_Update( BLEU, i);
			delay_delay(TEMPS);
		}
	}
	return 0;
#endif
#ifdef ___TEST_PULSE___
	gpio_init();
	delay_init();
	gpio_led1_on();
	PWM_Init();
	PWM_Update( ROUGE,  -600 );
	PWM_Update( VERT,  -600 );
	PWM_Update( BLEU,  -600 );
	PWM_Start();
	PWM_pulse(ROUGE,1);
	PWM_pulse(VERT,1);
	PWM_pulse(BLEU,1);
	unsigned long previousTimeRouge=delay_time(),previousTimeBleu=delay_time(),previousTimeVert=delay_time();
	while(1)
	{
		if( (pwm_pulse & (0x7)))
		{
			if((delay_time()-previousTimeRouge) > TEMPS)
			{
				PWM_pulse_update(ROUGE);
				previousTimeRouge = delay_time();
			}
			if((delay_time()-previousTimeBleu) > TEMPS1)
			{
				PWM_pulse_update(BLEU);
				previousTimeBleu = delay_time();
			}
			if((delay_time()-previousTimeVert) > TEMPS2)
			{
				PWM_pulse_update(VERT);
				previousTimeVert = delay_time();
			}
		}
	}
	return 0;
#endif
}
