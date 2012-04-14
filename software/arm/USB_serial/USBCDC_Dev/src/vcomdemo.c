/*----------------------------------------------------------------------------
 *      Name:    vcomdemo.c
 *      Purpose: USB virtual COM port Demo
 *      Version: V1.20
 *----------------------------------------------------------------------------
 *      This software is supplied "AS IS" without any warranties, express,
 *      implied or statutory, including but not limited to the implied
 *      warranties of fitness for purpose, satisfactory quality and
 *      noninfringement. Keil extends you a royalty-free right to reproduce
 *      and distribute executable files created using this software for use
 *      on NXP Semiconductors LPC microcontroller devices only. Nothing else 
 *      gives you the right to use this software.
 *
 * Copyright (c) 2009 Keil - An ARM Company. All rights reserved.
 *---------------------------------------------------------------------------*/

#include <cr_section_macros.h>
#include <NXP/crp.h>

// Variable to store CRP value in. Will be placed automatically
// by the linker when "Enable Code Read Protect" selected.
// See crp.h header for more information
__CRP const unsigned int CRP_WORD = CRP_NO_CRP ;


#include "LPC17xx.h"    
#include "type.h"
#include "bootloader.h"

#include "usb.h"
#include "usbcfg.h"
#include "usbhw.h"
#include "usbcore.h"
#include "cdc.h"
#include "cdcuser.h"
#include "serial.h"
#include "vcomdemo.h"

#include "_LPC17xx.h"
#include "uart.h"

#include "delay.h"
#include "gpio.h"
#include "pwm.h"
#include "buffer.h"

#define TEMPO 5000
#define TEMPO2 50
#define TEMPS 1000

int debug_endpoint = 0;

unsigned long currentTime,previousTime;

//#include "lcd.h"
//uint32_t SystemFrequency;

/*
 * The task that handles the USB stack.
 */
//extern void vUSBTask();

/*----------------------------------------------------------------------------
 Initialises the VCOM port.
 Call this function before using VCOM_putchar or VCOM_getchar
 *---------------------------------------------------------------------------*/
void VCOM_Init(void) {
  CDC_Init (0);
  CDC_Init (1);
  CDC_Init (2);
  CDC_Init (3);
}


/*----------------------------------------------------------------------------
  Reads character from serial port buffer and writes to USB buffer
 *---------------------------------------------------------------------------*/
void VCOM0_Serial0_2_Usb(void) {
  static char serBuf [USB_CDC_BUFSIZE];
         int  numBytesRead, numAvailByte;
	
  ser0_AvailChar (&numAvailByte);
  if (numAvailByte > 0) {
    if (CDC0_DepInEmpty) {
      numBytesRead = ser0_Read (&serBuf[0], &numAvailByte);

      CDC0_DepInEmpty = 0;
	  USB_WriteEP (CDC0_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
  }
}

void VCOM1_Serial1_2_Usb(void) {
  static char serBuf [USB_CDC_BUFSIZE];
         int  numBytesRead, numAvailByte;

  ser1_AvailChar (&numAvailByte);
  if (numAvailByte > 0) {
    if (CDC1_DepInEmpty) {
      numBytesRead = ser1_Read (&serBuf[0], &numAvailByte);

      CDC1_DepInEmpty = 0;
	  USB_WriteEP (CDC1_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
  }
}

void VCOM2_Serial2_2_Usb(void) {
  static char serBuf [USB_CDC_BUFSIZE];
         int  numBytesRead, numAvailByte;

  ser2_AvailChar (&numAvailByte);
  if (numAvailByte > 0) {
    if (CDC2_DepInEmpty) {
      numBytesRead = ser2_Read (&serBuf[0], &numAvailByte);

      CDC2_DepInEmpty = 0;
	  USB_WriteEP (CDC2_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
  }
}

void VCOM3_Serial3_2_Usb(void) {
  static char serBuf [USB_CDC_BUFSIZE];
         int  numBytesRead, numAvailByte;


  ser3_AvailChar (&numAvailByte);
  if (numAvailByte > 0) {
    if (CDC3_DepInEmpty) {
      numBytesRead = ser3_Read (&serBuf[0], &numAvailByte);

      CDC3_DepInEmpty = 0;
	  USB_WriteEP (CDC3_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);

    }
  }
}

/*----------------------------------------------------------------------------
  Reads character from USB buffer and writes to serial port buffer
 *---------------------------------------------------------------------------*/
void VCOM0_Usb_2_Serial0(void) {
  static char serBuf [32];
         int  numBytesToRead, numBytesRead, numAvailByte;

  CDC0_OutBufAvailChar (&numAvailByte);
  if (numAvailByte > 0) {
      numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte; 
      numBytesRead = CDC0_RdOutBuf (&serBuf[0], &numBytesToRead);

      ser0_Write (&serBuf[0], &numBytesRead);
  }
}

void VCOM1_Usb_2_Serial1(void) {
  static char serBuf [32];
         int  numBytesToRead, numBytesRead, numAvailByte;

  CDC1_OutBufAvailChar (&numAvailByte);
  if (numAvailByte > 0) {
      numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
      numBytesRead = CDC1_RdOutBuf (&serBuf[0], &numBytesToRead);

      ser1_Write (&serBuf[0], &numBytesRead);
  }
}

void VCOM2_Usb_2_Serial2(void) {
  static char serBuf [32];
         int  numBytesToRead, numBytesRead, numAvailByte;

  CDC2_OutBufAvailChar (&numAvailByte);
  if (numAvailByte > 0) {
      numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
      numBytesRead = CDC2_RdOutBuf (&serBuf[0], &numBytesToRead);

      ser2_Write (&serBuf[0], &numBytesRead);
  }
}

void VCOM3_Usb_2_Serial3(void) {
  static char serBuf [32];
         int  numBytesToRead, numBytesRead, numAvailByte;

  CDC3_OutBufAvailChar (&numAvailByte);
  if (numAvailByte > 0) {
      numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
      numBytesRead = CDC3_RdOutBuf (&serBuf[0], &numBytesToRead);

      ser3_Write (&serBuf[0], &numBytesRead);
  }
}

/*----------------------------------------------------------------------------
  Reads character from USB buffer and writes back to USB buffer
 *---------------------------------------------------------------------------*/
void VCOM_Usb2Usb0(void){
    static char serBuf [32];
    int  numBytesToRead, numBytesRead, numAvailByte;

    /* Get USB VCOM received bytes */
    CDC0_OutBufAvailChar (&numAvailByte);
    if (numAvailByte > 0) {
            numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
            numBytesRead = CDC0_RdOutBuf (&serBuf[0], &numBytesToRead);

               /* Write bytes to USB VCOM */
               USB_WriteEP (CDC0_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
}

void VCOM_Usb2Usb1(void){
    static char serBuf [32];
    int  numBytesToRead, numBytesRead, numAvailByte;

    /* Get USB VCOM received bytes */
    CDC1_OutBufAvailChar (&numAvailByte);
    if (numAvailByte > 0) {
            numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
            numBytesRead = CDC1_RdOutBuf (&serBuf[0], &numBytesToRead);

               /* Write bytes to USB VCOM */
               USB_WriteEP (CDC1_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
}

void VCOM_Usb2Usb2(void){
    static char serBuf [32];
    int  numBytesToRead, numBytesRead, numAvailByte;

    /* Get USB VCOM received bytes */
    CDC2_OutBufAvailChar (&numAvailByte);
    if (numAvailByte > 0) {
            numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
            numBytesRead = CDC2_RdOutBuf (&serBuf[0], &numBytesToRead);

               /* Write bytes to USB VCOM */
               USB_WriteEP (CDC2_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
}

void VCOM_Usb2Usb3(void){
    static char serBuf [32];
    int  numBytesToRead, numBytesRead, numAvailByte;

    /* Get USB VCOM received bytes */
    CDC3_OutBufAvailChar (&numAvailByte);
    if (numAvailByte > 0) {
            numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
            numBytesRead = CDC3_RdOutBuf (&serBuf[0], &numBytesToRead);

               /* Write bytes to USB VCOM */
               USB_WriteEP (CDC3_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
}

/////////////////////////////////////////////////////////////////
void Wait4DevInt(unsigned long dwIntr)
{
	// wait for specific interrupt
	while ((LPC_USB->DevIntSt & dwIntr) != dwIntr);
	// clear the interrupt bits
	LPC_USB->DevIntClr = dwIntr;
}

void USBHwCmd(unsigned char bCmd)
{
	// clear CDFULL/CCEMTY
	LPC_USB->DevIntClr = (1<<5) | (1<<4);
	// write command code
	LPC_USB->CmdCode = 0x00000500 | (bCmd << 16);
	Wait4DevInt(1<<4);
}

void USBHwCmdWrite(unsigned char bCmd, unsigned short bData)
{
	// write command code
	USBHwCmd(bCmd);

	// write command data
	LPC_USB->CmdCode = 0x00000100 | (bData << 16);
	Wait4DevInt(1<<4);
}

void USBHwConnect(int fConnect)
{
	USBHwCmdWrite(0xFE, fConnect ? (1<<0) : 0);
}
//////////////////////////////////////////////////////////////

void VCOM_Usb2Usb4(void){
    static char serBuf [32];
    int  numBytesToRead, numBytesRead, numAvailByte;

    /* Get USB VCOM received bytes */
    CDC4_OutBufAvailChar (&numAvailByte);
    if (numAvailByte > 0) {
            numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
            numBytesRead = CDC4_RdOutBuf (&serBuf[0], &numBytesToRead);

            int i;
            for( i=0; i<numAvailByte;++i)
            {
            	USB_WriteEP (CDC4_DEP_IN, "trig_on", 7);
            	bufferWrite(serBuf[i]);
            }

           /* if (serBuf[0] == 'L')
            {
            	// Bootloader Mode
            	boot_buffer[0] = 0xAA;
            	boot_buffer[1] = 0xBB;
            	boot_buffer[2] = 0xCC;
            	boot_buffer[3] = 0xDD;
            	// usb_detach() + Reset CPU
            	NVIC_DisableIRQ(USB_IRQn);
            	USBHwConnect(FALSE);
            	//LPC_SC->PCONP&=0x7FFFFFFF;
            	//NVIC_SystemReset();

            }
            else if (serBuf[0] =='a')
            {
            	gpio_cam_trig_on();
            	gpio_led1_on();
            	USB_WriteEP (CDC4_DEP_IN, "trig_on", 7);
            }
            else if (serBuf[0] =='z')
            {
            	gpio_cam_trig_off();
            	gpio_led1_off();
            	USB_WriteEP (CDC4_DEP_IN, "trig_off", 8);
            }
            else if(serBuf[0] =='q')
            {
            	gpio_alim_cam_on();
            	gpio_led2_on();
            	USB_WriteEP (CDC4_DEP_IN, "cam_on", 6);
            }
            else if(serBuf[0] =='s')
            {
            	gpio_alim_cam_off();
            	gpio_led2_off();
            	USB_WriteEP (CDC4_DEP_IN, "cam_off", 7);
            }
            else if(serBuf[0] == 'e')
            {
            	gpio_cam_trig();
            	USB_WriteEP (CDC4_DEP_IN, "trig", 4);
            }

            else if(serBuf[0] == 'm')
            {
            	gpio_cam_trig_output();
            	USB_WriteEP (CDC4_DEP_IN, "trig_input", 10);
            }

            else if(serBuf[0] == 'p')
            {
            	gpio_cam_trig_output();
            	USB_WriteEP (CDC4_DEP_IN, "trig_output", 11);
            }
            else
            {
               USB_WriteEP (CDC4_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
            }*/
    }
}

/*----------------------------------------------------------------------------
  checks the serial state and initiates notification
 *---------------------------------------------------------------------------*/
void VCOM0_CheckSerial0_State (void) {
         unsigned short temp;
  static unsigned short serialState;

  temp = CDC0_GetSerialState();
  if (serialState != temp) {
     serialState = temp;
     CDC0_NotificationIn();                  // send SERIAL_STATE notification
  }
}

void VCOM1_CheckSerial1_State (void) {
         unsigned short temp;
  static unsigned short serialState;

  temp = CDC1_GetSerialState();
  if (serialState != temp) {
     serialState = temp;
     CDC1_NotificationIn();                  // send SERIAL_STATE notification
  }
}

volatile uint32_t time_current;

/*----------------------------------------------------------------------------
  Main Program
 *---------------------------------------------------------------------------*/
int main (void) {
	/*while(1)
	{
		gpio_led3_off();
		gpio_led1_on();
		delay_delay(TEMPS);
		gpio_led1_off();
		gpio_led2_on();
		delay_delay(TEMPS);
		gpio_led2_off();
		gpio_led3_on();
		delay_delay(TEMPS);
	}*/

	/*PWM_Init();
	PWM_Update( ROUGE,  -600 );
	  PWM_Update( VERT,  -600 );
	  PWM_Update( BLEU,  -600 );
	  PWM_Start();*/
	gpio_init();
	delay_init();
			gpio_led1_on();
			previousTime = delay_time();
			gpio_alim_cam_on();
			delay_delay(500);
			gpio_led2_on();
			gpio_cam_trig();
			int ledState2 = 0;
  /*	UART0/VCOM0 & UART1/VCOM1 Port are initialized @ 115200 bps */

  /* SystemClockUpdate() updates the SystemFrequency variable */
  SystemClockUpdate();

  VCOM_Init();                              // VCOM Initialization

  USB_Init();                               // USB Initialization
  USB_Reset();
  USB_Connect(TRUE);                        // USB Connect
  while (!USB_Configuration) ;              // wait until USB is configured

  //printf( "USB_Configuration ok\n\r");


  while (1) {
	VCOM0_Serial0_2_Usb();                // read serial port and initiate USB event
	VCOM0_Usb_2_Serial0();

	VCOM1_Serial1_2_Usb();                // read serial port and initiate USB event
	VCOM1_Usb_2_Serial1();

	VCOM2_Serial2_2_Usb();                // read serial port and initiate USB event
	VCOM2_Usb_2_Serial2();

	VCOM3_Serial3_2_Usb();                // read serial port and initiate USB event
	VCOM3_Usb_2_Serial3();


	if( bufferAvailable() )
	{
		char *octet = NULL;
		if( bufferRead(octet ) == 0)
			traitement(*octet );
	}


	////////////////
	//VCOM_Usb2Usb0();            				// Read USB and write to USB
    //VCOM_Usb2Usb1();            				// Read USB and write to USB
   // VCOM_Usb2Usb2();            				// Read USB and write to USB
   // VCOM_Usb2Usb3();            				// Read USB and write to USB
    VCOM_Usb2Usb4();            				// Read USB and write to USB
  } // end while											   
} // end main ()
