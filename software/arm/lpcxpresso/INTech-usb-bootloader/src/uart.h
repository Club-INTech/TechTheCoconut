//*****************************************************************************
//   +--+       
//   | ++----+   
//   +-++    |  
//     |     |  
//   +-+--+  |   
//   | +--+--+  
//   +----+    Copyright (c) 2009 Code Red Technologies Ltd. 
//
// UART example header file
//
// Software License Agreement
// 
// The software is owned by Code Red Technologies and/or its suppliers, and is 
// protected under applicable copyright laws.  All rights are reserved.  Any 
// use in violation of the foregoing restrictions may subject the user to criminal 
// sanctions under applicable laws, as well as to civil liability for the breach 
// of the terms and conditions of this license.
// 
// THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED
// OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
// USE OF THIS SOFTWARE FOR COMMERCIAL DEVELOPMENT AND/OR EDUCATION IS SUBJECT
// TO A CURRENT END USER LICENSE AGREEMENT (COMMERCIAL OR EDUCATIONAL) WITH
// CODE RED TECHNOLOGIES LTD. 
//
//*****************************************************************************

#ifndef UART_H_
#define UART_H_

#define TER_TXEN	0x01

#define LSR_RDR		0x01
#define LSR_OE		0x02
#define LSR_PE		0x04
#define LSR_FE		0x08
#define LSR_BI		0x10
#define LSR_THRE	0x20
#define LSR_TEMT	0x40
#define LSR_RXFE	0x80

/* Uart line control register bit descriptions */
#define LCR_WORDLENTH_BIT         0
#define LCR_STOPBITSEL_BIT        2
#define LCR_PARITYENBALE_BIT      3
#define LCR_PARITYSEL_BIT         4
#define LCR_BREAKCONTROL_BIT      6
#define LCR_DLAB_BIT              7

/* Uart Interrupt Identification */
#define IIR_RSL                   0x3
#define IIR_RDA                   0x2
#define IIR_CTI                   0x6
#define IIR_THRE                  0x1

/* Uart Interrupt Enable Type*/
#define IER_RBR                   0x1
#define IER_THRE                  0x2
#define IER_RLS                   0x4

/* Uart Fifo control register */
#define FCR_FIFOEN                0x1
#define FCR_FIFORXR               0x2
#define FCR_FIFOTXR               0x4

/* Uart Receiver Errors*/
#define RC_FIFO_OVERRUN_ERR       0x1
#define RC_OVERRUN_ERR            0x2
#define RC_PARITY_ERR             0x4
#define RC_FRAMING_ERR            0x8
#define RC_BREAK_IND              0x10

#define BR_LOOKUP_SIZE 72

// PCUART0
#define PCUART0_POWERON (1 << 3)
#define PCLK_UART0 6
#define PCLK_UART0_MASK (3 << PCLK_UART0)

// PCUART1
#define PCUART1_POWERON (1 << 4)
#define PCLK_UART1 8
#define PCLK_UART1_MASK (3 << PCLK_UART1)

// PCUART2
#define PCUART2_POWERON (1 << 24)
#define PCLK_UART2 16
#define PCLK_UART2_MASK (3 << PCLK_UART2)

// PCUART3
#define PCUART3_POWERON (1 << 25)
#define PCLK_UART3 18
#define PCLK_UART3_MASK (3 << PCLK_UART3)

// ***********************
// Uart 0 functions
void UART0_Init(int baudrate);
void UART0_Sendchar(char c);
char UART0_Getchar();
int  UART0_Getchar_NonBlocking();
int  UART0_isDataAvailable();
void UART0_PrintString(char *pcString);


// Uart 1 functions
void UART1_Init(int baudrate);
void UART1_Sendchar(char c);
char UART1_Getchar();
int  UART1_Getchar_NonBlocking();
int  UART1_isDataAvailable();
void UART1_PrintString(char *pcString);

// Uart 2 functions
void UART2_Init(int baudrate);
void UART2_Sendchar(char c);
char UART2_Getchar();
int  UART2_Getchar_NonBlocking();
int  UART2_isDataAvailable();
void UART2_PrintString(char *pcString);

// Uart 3 functions
void UART3_Init(int baudrate);
void UART3_Sendchar(char c);
char UART3_Getchar();
int  UART3_Getchar_NonBlocking();
int  UART3_isDataAvailable();
void UART3_PrintString(char *pcString);

// Generic Uart functions
int initUart(int uart, int baudrate);
int UART_Sendchar(int uart, char c);
char UART_Getchar(int uart);
int  UART_Getchar_NonBlocking(int uart);
int  UART_isDataAvailable(int uart);
int UART_PrintString(int uart, char *pcString);

#endif /*UART_H_*/
