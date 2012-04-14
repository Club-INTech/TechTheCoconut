/*----------------------------------------------------------------------------
 *      Name:    serial.c
 *      Purpose: serial port handling for LPC17xx
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
#include "LPC17xx.h"                                   // LPC17xx definitions
//#include "type.h"
#include "serial.h"
#include "uart.h"
#include "gpio.h"

#define UART1 1

//#define __V2__

/*----------------------------------------------------------------------------
  Defines for ring buffers
 *---------------------------------------------------------------------------*/
#define SER_BUF_SIZE               (128)               // serial buffer in bytes (power 2)
#define SER_BUF_MASK               (SER_BUF_SIZE-1ul)  // buffer size mask

/* Buffer read / write macros */
#define SER_BUF_RESET(serBuf)      (serBuf.rdIdx = serBuf.wrIdx = 0)
#define SER_BUF_WR(serBuf, dataIn) (serBuf.data[SER_BUF_MASK & serBuf.wrIdx++] = (dataIn))
#define SER_BUF_RD(serBuf)         (serBuf.data[SER_BUF_MASK & serBuf.rdIdx++])
#define SER_BUF_EMPTY(serBuf)      (serBuf.rdIdx == serBuf.wrIdx)
#define SER_BUF_FULL(serBuf)       (serBuf.rdIdx == serBuf.wrIdx+1)
#define SER_BUF_COUNT(serBuf)      (SER_BUF_MASK & (serBuf.wrIdx - serBuf.rdIdx))

// buffer type
typedef struct __SER_BUF_T {
  unsigned char data[SER_BUF_SIZE];
  unsigned int wrIdx;
  unsigned int rdIdx;
} SER_BUF_T;

unsigned long          ser0_txRestart;                  // NZ if TX restart is required
unsigned short         ser0_lineState;                  // ((msr << 8) | (lsr))
SER_BUF_T              ser0_out;                        // Serial data buffers
SER_BUF_T              ser0_in;

unsigned long          ser1_txRestart;                  // NZ if TX restart is required
unsigned short         ser1_lineState;                  // ((msr << 8) | (lsr))
SER_BUF_T              ser1_out;                        // Serial data buffers
SER_BUF_T              ser1_in;

unsigned long          ser2_txRestart;                  // NZ if TX restart is required
unsigned short         ser2_lineState;                  // ((msr << 8) | (lsr))
SER_BUF_T              ser2_out;                        // Serial data buffers
SER_BUF_T              ser2_in;

unsigned long          ser3_txRestart;                  // NZ if TX restart is required
unsigned short         ser3_lineState;                  // ((msr << 8) | (lsr))
SER_BUF_T              ser3_out;                        // Serial data buffers
SER_BUF_T              ser3_in;


/*----------------------------------------------------------------------------
  open the serial port
 *---------------------------------------------------------------------------*/
void ser_OpenPort (char portNum) {
 
	if ( portNum == 0 )
	{
		NVIC_DisableIRQ(UART0_IRQn);					// Disable the UART Interrupt
		initUart(portNum, 115200);
		SER_BUF_RESET(ser0_out);                  		// reset out buffer
		SER_BUF_RESET(ser0_in);                     	// reset in buffer
		ser0_txRestart = 1;								// TX fifo is empty
		NVIC_EnableIRQ(UART0_IRQn);						// Enable the UART Interrupt
	}
	else if ( portNum == 1 )
	{
		NVIC_DisableIRQ(UART1_IRQn);					// Disable the UART Interrupt
		initUart(portNum, 9600);
		SER_BUF_RESET(ser1_out);            			// reset out buffer
		SER_BUF_RESET(ser1_in);            				// reset in buffer
		ser1_txRestart = 1;               			 	// TX fifo is empty
		NVIC_EnableIRQ(UART1_IRQn);						// Enable the UART Interrupt
	}
	else if ( portNum == 2 )
	{
		NVIC_DisableIRQ(UART2_IRQn);					// Disable the UART Interrupt
		initUart(portNum, 9600);
		SER_BUF_RESET(ser2_out);            			// reset out buffer
		SER_BUF_RESET(ser2_in);            				// reset in buffer
		ser2_txRestart = 1;               			 	// TX fifo is empty
		NVIC_EnableIRQ(UART2_IRQn);						// Enable the UART Interrupt
	}
	else if ( portNum == 3 )
	{
		NVIC_DisableIRQ(UART3_IRQn);					// Disable the UART Interrupt
		initUart(portNum, 115200);
		SER_BUF_RESET(ser3_out);            			// reset out buffer
		SER_BUF_RESET(ser3_in);            				// reset in buffer
		ser3_txRestart = 1;               			 	// TX fifo is empty
		NVIC_EnableIRQ(UART3_IRQn);						// Enable the UART Interrupt
	}

	return;
}

/*----------------------------------------------------------------------------
  close the serial port
 *---------------------------------------------------------------------------*/
void ser_ClosePort (char portNum ) {
  if ( portNum == 0 )
  {
	/* POrt 0 */
	LPC_PINCON->PINSEL0 &= ~0x000000F0;
	/* Disable the interrupt in the VIC and UART controllers */
	LPC_UART0->IER = 0;
	NVIC_DisableIRQ(UART0_IRQn);
  }
  else
  {
	/* Port 1 */
	LPC_PINCON->PINSEL4 &= ~0x0000000F;
	/* Disable the interrupt in the VIC and UART controllers */
	LPC_UART1->IER = 0;
	NVIC_DisableIRQ(UART1_IRQn);
  }	
  return;
}

/*----------------------------------------------------------------------------
  initialize the serial port
 *---------------------------------------------------------------------------*/
void ser_InitPort0 (unsigned long baudrate, unsigned int  databits,
                  unsigned int  parity,   unsigned int  stopbits) {

  unsigned char lcr_p, lcr_s, lcr_d;
  unsigned int dll;
  unsigned int pclkdiv, pclk;
  
  switch (databits) {
    case 5:                                            // 5 Data bits
      lcr_d = 0x00;
    break;
    case 6:                                            // 6 Data bits
      lcr_d = 0x01;
    break;
    case 7:                                            // 7 Data bits
      lcr_d = 0x02;
    break;
    case 8:                                            // 8 Data bits
    default:
      lcr_d = 0x03;
    break;
  }

  switch (stopbits) {
    case 1:                                            // 1,5 Stop bits
    case 2:                                            // 2   Stop bits
      lcr_s = 0x04;
    break;
    case 0:                                            // 1   Stop bit
    default:
      lcr_s = 0x00;
    break;
  }

  switch (parity) {
    case 1:                                            // Parity Odd
      lcr_p = 0x08;
    break;
    case 2:                                            // Parity Even
      lcr_p = 0x18;
    break;
    case 3:                                            // Parity Mark
      lcr_p = 0x28;
    break;
    case 4:                                            // Parity Space
      lcr_p = 0x38;
    break;
    case 0:                                            // Parity None
    default:
      lcr_p = 0x00;
    break;
  }

  SER_BUF_RESET(ser0_out);                              // reset out buffer
  SER_BUF_RESET(ser0_in);                               // reset in buffer
  
  /* Bit 6~7 is for UART0 */
  pclkdiv = (LPC_SC->PCLKSEL0 >> 6) & 0x03;

  switch ( pclkdiv )
  {
	case 0x00:
	default:
#ifdef __V2__
	  pclk = SystemCoreClock/4;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/4;
#endif
	  break;
	case 0x01:
#ifdef __V2__
	  pclk = SystemCoreClock;
#endif
#ifndef __V2__
	  pclk = SystemFrequency;
#endif
	  break;
	case 0x02:
#ifdef __V2__
	  pclk = SystemCoreClock/2;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/2;
#endif
	  break;
	case 0x03:
#ifdef __V2__
	  pclk = SystemCoreClock/8;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/8;
#endif
	  break;
  }

  dll = (pclk/16)/ baudrate;	/*baud rate */
  LPC_UART0->FDR = 0;                             // Fractional divider not used
  LPC_UART0->LCR = 0x80 | lcr_d | lcr_p | lcr_s;  // Data bits, Parity,   Stop bit
  LPC_UART0->DLL = dll;                           // Baud Rate depending on PCLK
  LPC_UART0->DLM = (dll >> 8);                    // High divisor latch
  LPC_UART0->LCR = 0x00 | lcr_d | lcr_p | lcr_s;  // DLAB = 0
  LPC_UART0->IER = 0x03;                          // Enable TX/RX interrupts

  LPC_UART0->FCR = 0x07;				/* Enable and reset TX and RX FIFO. */
  ser0_txRestart = 1;                                   // TX fifo is empty

  /* Enable the UART Interrupt */
  NVIC_EnableIRQ(UART0_IRQn);
  return;
}

/*----------------------------------------------------------------------------
  initialize the serial port
 *---------------------------------------------------------------------------*/
void ser_InitPort1 (unsigned long baudrate, unsigned int  databits,
                  unsigned int  parity,   unsigned int  stopbits) {

  unsigned char lcr_p, lcr_s, lcr_d;
  unsigned int dll;
  unsigned int pclkdiv, pclk;
  
  switch (databits) {
    case 5:                                            // 5 Data bits
      lcr_d = 0x00;
    break;
    case 6:                                            // 6 Data bits
      lcr_d = 0x01;
    break;
    case 7:                                            // 7 Data bits
      lcr_d = 0x02;
    break;
    case 8:                                            // 8 Data bits
    default:
      lcr_d = 0x03;
    break;
  }

  switch (stopbits) {
    case 1:                                            // 1,5 Stop bits
    case 2:                                            // 2   Stop bits
      lcr_s = 0x04;
    break;
    case 0:                                            // 1   Stop bit
    default:
      lcr_s = 0x00;
    break;
  }

  switch (parity) {
    case 1:                                            // Parity Odd
      lcr_p = 0x08;
    break;
    case 2:                                            // Parity Even
      lcr_p = 0x18;
    break;
    case 3:                                            // Parity Mark
      lcr_p = 0x28;
    break;
    case 4:                                            // Parity Space
      lcr_p = 0x38;
    break;
    case 0:                                            // Parity None
    default:
      lcr_p = 0x00;
    break;
  }

  SER_BUF_RESET(ser1_out);                              // reset out buffer
  SER_BUF_RESET(ser1_in);                               // reset in buffer
  
  /* Bit 8,9 are for UART1 */
  pclkdiv = (LPC_SC->PCLKSEL0 >> 8) & 0x03;

  switch ( pclkdiv )
  {
	case 0x00:
	default:
#ifdef __V2__
	  pclk = SystemCoreClock/4;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/4;
#endif
	  break;
	case 0x01:
#ifdef __V2__
	  pclk = SystemCoreClock;
#endif
#ifndef __V2__
	  pclk = SystemFrequency;
#endif
	  break;
	case 0x02:
#ifdef __V2__
	  pclk = SystemCoreClock/2;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/2;
#endif
	  break;
	case 0x03:
#ifdef __V2__
	  pclk = SystemCoreClock/8;
#endif
#ifndef __V2__
	  pclk = SystemFrequency/8;
#endif
	  break;
  }

  dll = (pclk/16)/baudrate ;	/*baud rate */
  //LPC_UART1->FDR = 0;                             // Fractional divider not used
  LPC_UART1->FDR = 193;	//((mulFracDivOptimal << 4) & 0xF0) | (dividerAddOptimal & 0x0F)

  LPC_UART1->LCR = 0x80 | lcr_d | lcr_p | lcr_s;  // Data bits, Parity,   Stop bit
  LPC_UART1->DLL = 6; // dll % 256;                   // Baud Rate depending on PCLK
  LPC_UART1->DLM = 0; // dll / 256;                   // High divisor latch
  LPC_UART1->LCR = 0x00 | lcr_d | lcr_p | lcr_s;  // DLAB = 0
  LPC_UART1->IER = 0x03;                          // Enable TX/RX interrupts

  LPC_UART1->FCR = 0x07;				/* Enable and reset TX and RX FIFO. */
  ser1_txRestart = 1;                                   // TX fifo is empty

  /* Enable the UART Interrupt */
  NVIC_EnableIRQ(UART1_IRQn);
  return;
}


/*----------------------------------------------------------------------------
  read data from serial port
 *---------------------------------------------------------------------------*/
int ser0_Read (char *buffer, const int *length) {
  int bytesToRead, bytesRead;
  
  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;

  while (bytesToRead--) {
    while (SER_BUF_EMPTY(ser0_in));                     // Block until data is available if none
    *buffer++ = SER_BUF_RD(ser0_in);
  }
  return (bytesRead);  
}

int ser1_Read (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;

  while (bytesToRead--) {
    while (SER_BUF_EMPTY(ser1_in));                     // Block until data is available if none
    *buffer++ = SER_BUF_RD(ser1_in);
  }
  return (bytesRead);
}

int ser2_Read (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;

  while (bytesToRead--) {
    while (SER_BUF_EMPTY(ser2_in));                     // Block until data is available if none
    *buffer++ = SER_BUF_RD(ser2_in);
  }
  return (bytesRead);
}


int ser3_Read (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;

  while (bytesToRead--) {
    while (SER_BUF_EMPTY(ser3_in));                     // Block until data is available if none
    *buffer++ = SER_BUF_RD(ser3_in);
  }
  return (bytesRead);
}


/*----------------------------------------------------------------------------
  write data to the serial port
 *---------------------------------------------------------------------------*/
int ser0_Write (const char *buffer, int *length) {
  int  bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;

  while (!SER_BUF_EMPTY(ser0_out));               		// Block until space is available if none
  while (bytesToWrite) {
      SER_BUF_WR(ser0_out, *buffer++);            		// Read Rx FIFO to buffer
      bytesToWrite--;
  }     

  if (ser0_txRestart) {
    ser0_txRestart = 0;
	LPC_UART0->THR = SER_BUF_RD(ser0_out);             	// Write to the Tx Register
  }

  return (bytesWritten); 
}

int ser1_Write (const char *buffer, int *length) {
  int  bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;

  while (!SER_BUF_EMPTY(ser1_out));               		// Block until space is available if none
  while (bytesToWrite) {
      SER_BUF_WR(ser1_out, *buffer++);            		// Read Rx FIFO to buffer
      bytesToWrite--;
  }

  if (ser1_txRestart) {
    ser1_txRestart = 0;
    LPC_UART1->THR = SER_BUF_RD(ser1_out);             	// Write to the Tx Register
  }

  return (bytesWritten);
}

int ser2_Write (const char *buffer, int *length) {
  int  bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;

  while (!SER_BUF_EMPTY(ser2_out));               		// Block until space is available if none
  while (bytesToWrite) {
      SER_BUF_WR(ser2_out, *buffer++);            		// Read Rx FIFO to buffer
      bytesToWrite--;
  }

  if (ser2_txRestart) {
    ser2_txRestart = 0;
    LPC_UART2->THR = SER_BUF_RD(ser2_out);             	// Write to the Tx Register
  }

  return (bytesWritten);
}

int ser3_Write (const char *buffer, int *length) {
  int  bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;

  while (!SER_BUF_EMPTY(ser3_out));               		// Block until space is available if none
  while (bytesToWrite) {
      SER_BUF_WR(ser3_out, *buffer++);            		// Read Rx FIFO to buffer
      bytesToWrite--;
  }

  if (ser3_txRestart) {
    ser3_txRestart = 0;
    LPC_UART3->THR = SER_BUF_RD(ser3_out);             	// Write to the Tx Register
  }

  return (bytesWritten);
}

/*----------------------------------------------------------------------------
  check if character(s) are available at the serial interface
 *---------------------------------------------------------------------------*/
void ser0_AvailChar (int *availChar) {

  *availChar = SER_BUF_COUNT(ser0_in);

}

void ser1_AvailChar (int *availChar) {

  *availChar = SER_BUF_COUNT(ser1_in);

}

void ser2_AvailChar (int *availChar) {

  *availChar = SER_BUF_COUNT(ser2_in);

}

void ser3_AvailChar (int *availChar) {

  *availChar = SER_BUF_COUNT(ser3_in);

}

/*----------------------------------------------------------------------------
  read the line state of the serial port
 *---------------------------------------------------------------------------*/
void ser0_LineState (unsigned short *lineState) {

  *lineState = ser0_lineState;
  ser0_lineState = 0;

}

void ser1_LineState (unsigned short *lineState) {

  *lineState = ser1_lineState;
  ser1_lineState = 0;

}

void ser2_LineState (unsigned short *lineState) {

  *lineState = ser2_lineState;
  ser2_lineState = 0;

}

void ser3_LineState (unsigned short *lineState) {

  *lineState = ser3_lineState;
  ser3_lineState = 0;

}

/*----------------------------------------------------------------------------
  serial port 0 interrupt
 *---------------------------------------------------------------------------*/
void UART0_IRQHandler(void) 
{ 
  volatile unsigned long iir;

  iir = LPC_UART0->IIR;

  if ((iir & 0x4) || (iir & 0xC)) {            // RDA or CTI pending
    while (LPC_UART0->LSR & 0x01) {                 // Rx FIFO is not empty
      SER_BUF_WR(ser0_in, LPC_UART0->RBR);           // Read Rx FIFO to buffer
    }
  }
  if ((iir & 0x2)) {                           // TXMIS pending
	if (SER_BUF_COUNT(ser0_out) != 0) {
      LPC_UART0->THR = SER_BUF_RD(ser0_out);         // Write to the Tx FIFO
      ser0_txRestart = 0;
    }
	else {
      ser0_txRestart = 1;
	}
  }
  ser0_lineState = LPC_UART0->LSR & 0x1E;            // update linestate
  return;
}

/*----------------------------------------------------------------------------
  serial port 1 interrupt
 *---------------------------------------------------------------------------*/
void UART1_IRQHandler(void) 
{ 
  volatile unsigned long iir;
  
  iir = LPC_UART1->IIR;
   
  if ((iir & 0x4) || (iir & 0xC)) {            // RDA or CTI pending
    while (LPC_UART1->LSR & 0x01) {                 // Rx FIFO is not empty
      SER_BUF_WR(ser1_in, LPC_UART1->RBR);           // Read Rx FIFO to buffer
    }
  }
  if ((iir & 0x2)) {                           // TXMIS pending
	if (SER_BUF_COUNT(ser1_out) != 0) {
      LPC_UART1->THR = SER_BUF_RD(ser1_out);         // Write to the Tx FIFO
      ser1_txRestart = 0;
    }
	else {
      ser1_txRestart = 1;
	}
  }
  ser1_lineState = ((LPC_UART1->MSR<<8)|LPC_UART1->LSR) & 0xE01E;    // update linestate*/
  return;
}

/*----------------------------------------------------------------------------
  serial port 2 interrupt
 *---------------------------------------------------------------------------*/
void UART2_IRQHandler(void)
{
  volatile unsigned long iir;

  iir = LPC_UART2->IIR;

  if ((iir & 0x4) || (iir & 0xC)) {            // RDA or CTI pending
    while (LPC_UART2->LSR & 0x01) {                 // Rx FIFO is not empty
      SER_BUF_WR(ser2_in, LPC_UART2->RBR);           // Read Rx FIFO to buffer
    }
  }
  if ((iir & 0x2)) {                           // TXMIS pending
	if (SER_BUF_COUNT(ser2_out) != 0) {
      LPC_UART2->THR = SER_BUF_RD(ser2_out);         // Write to the Tx FIFO
      ser2_txRestart = 0;
    }
	else {
      ser2_txRestart = 1;
	}
  }
  ser2_lineState = LPC_UART2->LSR & 0x1E;            // update linestate*/
  return;
}

/*----------------------------------------------------------------------------
  serial port 3 interrupt
 *---------------------------------------------------------------------------*/
void UART3_IRQHandler(void)
{
  volatile unsigned long iir;
  iir = LPC_UART3->IIR;

  if ((iir & 0x4) || (iir & 0xC)) {            // RDA or CTI pending
    while (LPC_UART3->LSR & 0x01) {                 // Rx FIFO is not empty
      SER_BUF_WR(ser3_in, LPC_UART3->RBR);           // Read Rx FIFO to buffer
    }
  }
  if ((iir & 0x2)) {                           // TXMIS pending
	if (SER_BUF_COUNT(ser3_out) != 0) {
      LPC_UART3->THR = SER_BUF_RD(ser3_out);         // Write to the Tx FIFO
      ser3_txRestart = 0;
    }
	else {
      ser3_txRestart = 1;
	}
  }
  ser3_lineState = LPC_UART3->LSR & 0x1E;            // update linestate
  return;
}

