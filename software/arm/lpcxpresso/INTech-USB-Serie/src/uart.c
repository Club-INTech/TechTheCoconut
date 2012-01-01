#include "LPC17xx.h"
#include <string.h>
#include <stdio.h>
#include "uart.h"


//Tables for looking up fractional baud rate values.
float FRList[BR_LOOKUP_SIZE] = {1.000,1.067,1.071,1.077,1.083,1.091,1.100,1.111,1.125,1.133,1.143,1.154,1.167,1.182,1.200,1.214,1.222,1.231,1.250,
	1.267,1.273,1.286,1.300,1.308,1.333,1.357,1.364,1.375,1.385,1.400,1.417,1.429,1.444,1.455,1.462,1.467,1.500,1.533,1.538,1.545,1.556,
	1.571,1.583,1.600,1.615,1.625,1.636,1.643,1.667,1.692,1.700,1.714,1.727,1.733,1.750,1.769,1.778,1.786,1.800,1.818,1.833,1.846,1.857,
	1.867,1.875,1.889,1.900,1.909,1.917,1.923,1.929,1.933};
float DIVADDVALList[BR_LOOKUP_SIZE] = {0.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0,2.0,1.0,2.0,1.0,3.0,2.0,3.0,1.0,4.0,3.0,2.0,3.0,4.0,1.0,5.0,4.0,3.0,
	5.0,2.0,5.0,3.0,4.0,5.0,6.0,7.0,1.0,8.0,7.0,6.0,5.0,4.0,7.0,3.0,8.0,5.0,7.0,9.0,2.0,9.0,7.0,5.0,8.0,11.0,3.0,10.0,7.0,11.0,4.0,9.0,5.0,
	11.0,6.0,13.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0};
float MULVALList[BR_LOOKUP_SIZE] = {1.0,15.0,14.0,13.0,12.0,11.0,10.0,9.0,8.0,15.0,7.0,13.0,6.0,11.0,5.0,14.0,9.0,13.0,4.0,15.0,11.0,7.0,10.0,13.0,3.0,
	14.0,11.0,8.0,13.0,5.0,12.0,7.0,9.0,11.0,13.0,15.0,2.0,15.0,13.0,11.0,9.0,7.0,12.0,5.0,13.0,8.0,11.0,14.0,3.0,13.0,10.0,7.0,11.0,15.0,
	4.0,13.0,9.0,14.0,5.0,11.0,6.0,13.0,7.0,15.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0};

unsigned char uart1_etat = 0;

/**
 * Convert a float value to an ascii string.
 * Gives six decimal places resolution.
 */
static int ftoa(float v, char *ftoaBuf, int ftoaBufLen) {
	memset(ftoaBuf,0,ftoaBufLen);
	int intV = (int)v;
	int fractV = ((v-intV)*1000000);
	sprintf(ftoaBuf,"%d.%d",intV, fractV);
	return 0;
}

/**
 * Print a float value. For use when scanf lib function does not support floats.
 */
static int printfFloat(float v) {
	char fBuf[40];
	ftoa(v, fBuf, 40);
	printf("%s",fBuf);
	return 0;
}

/**
 * Print a debug message of a float value.
 */
static int debugPrintFloat(char *msg, float v) {
	printf(msg);
	printfFloat(v);
	printf("\n\r");
	return 0;
}

/**
 * Return 1 if the double is an int value, 0 if not
 */
static int isIntValue(double value) {
	int intValue = (int)value;
	if( value == intValue ) {
		return 1;
	}
	return 0;
}

/*
 * Get the fraction values for the given FRest value.
 */
static int getFRValues(double FRest, float *divAddVal, float *mulVal) {
	float lastDiff = -1;
	float thisDiff;
	int index;
	//Look through the lookup table and find the index of the value
	//that provides the smallest difference between the FRest value
	//and the lookup table value.
	for( index=0 ; index<BR_LOOKUP_SIZE ; index++ ) {
		if( FRest > FRList[index] ) {
			thisDiff = FRest-FRList[index];
		}
		else {
			thisDiff = FRList[index]-FRest;
		}
		if( lastDiff != -1 && thisDiff > lastDiff ) {
			//Set the fractional values required
			*divAddVal=DIVADDVALList[index-1];
			*mulVal=MULVALList[index-1];
			return 0;
		}
		lastDiff=thisDiff;
	}
	return -1;
}

/*
 * Get the fraction values required to set an accurate BR
 *
 * Return -1 on error, 0 on success.
 */
static int getFractionValues(int pclk, int baudRate, int *dlEst, float *divAddVal, float *mulVal) {
	double  dlEstFloat = pclk/(16.0*baudRate);
	double 	FRestSeed = 1.5;
	double  FRest;
	int 	DLest;

	//If this pclk and baud rate give and integer division
	//we don't need the fractional calculation
	if( isIntValue(dlEstFloat) ) {
		*dlEst = (int)dlEstFloat;
		*divAddVal=0.0;
		*mulVal=1.0;
		return 0;
	}

	while(1) {
		DLest = (int)(pclk/(16.0*baudRate*FRestSeed));
		FRest = pclk/(16.0*baudRate*DLest);
		//If we have the required accuracy
		if( FRest >= 1.1 && FRest < 1.9) {
			break;
		}

		if( FRestSeed <= 1.5 ) {
			FRestSeed-=0.001;
			if( FRestSeed < 1.1 ) {
				FRestSeed=1.5001;
			}
		}
		else {
			FRestSeed=FRestSeed+0.001;
			if( FRestSeed >= 1.9 ) {
				return -1;
			}
		}
	}
	*dlEst=(int)DLest;
	return getFRValues(FRest, divAddVal, mulVal);
}

/*********************** Start UART 0 functions *******************************/
/*
 * Init Uart0
 * P0.2 = TXD
 * p0.3 = RXD
 *
 * The serial port is set to 8 data bits, 1 stop bit, no parity. I thought about
 * the ability to set these through this function but decided not to until it was
 * needed in order to keep the interface as simple as possible. No need to add
 * complexity that is not required.
 *
 * Return -1 on error, 0 on success.
 */
int initUart0(int baudRate) {
	int 	pclk;
	int 	dlEest;
	float 	divAddVal, mulVal;

	// PCLK_UART0 is being set = SystemCoreClock
#ifdef __V2__
	pclk = SystemCoreClock;
#endif
#ifndef __V2__
	pclk = SystemFrequency;
#endif

	//Get the correct fractional values for the given pclk and required baud rate
	if( getFractionValues(pclk, baudRate, &dlEest, &divAddVal, &mulVal) == -1 ) {
		return -1;
	}

	// Turn on power to UART0
	LPC_SC->PCONP |=  PCUART0_POWERON;

	// Turn on UART0 peripheral clock
	LPC_SC->PCLKSEL0 &= ~(PCLK_UART0_MASK);
	LPC_SC->PCLKSEL0 |=  (1 << PCLK_UART0);     // PCLK_periph = CCLK

	// Set PINSEL0 so that P0.2 = TXD0
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 4);
	LPC_PINCON->PINSEL0 |= ( 1L << 4);
	// Set PINSEL0 so that P0.3 = RXD0
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 6);
	LPC_PINCON->PINSEL0 |= ( 1L << 6);

	LPC_UART0->LCR = 0x83;		// 8 bits, no Parity, 1 Stop bit, DLAB=1
	LPC_UART0->DLM = dlEest / 256;
	LPC_UART0->DLL = dlEest % 256;
	//Setup the fractional divider register
	LPC_UART0->FDR = (((int)mulVal)<<4)|(int)divAddVal;
	LPC_UART0->LCR = 0x03;		// 8 bits, no Parity, 1 Stop bit DLAB = 0
	LPC_UART0->FCR = 0x07;		// Enable and reset TX and RX FIFO

	LPC_UART0->IER = 0x03;                          // Enable TX/RX interrupts

	//Debug code
	//Calc actual baud rate achieved
	//int uartBaudRate = pclk/( 16*dlEest*(1+(divAddVal/mulVal)) );
	//printf("\ndlEest         =%d\n\rSystemCoreClock=%d\nuartBaudRate=%d\n\rpclk=%d\n\r",dlEest,SystemCoreClock,uartBaudRate,pclk);

	return 0;
}

// ***********************
// Function to send character over UART
void UART0_Sendchar(char c)
{
	while( (LPC_UART0->LSR & LSR_THRE) == 0 );	// Block until tx empty

	LPC_UART0->THR = c;
}

// ***********************
// Function to get character from UART
char UART0_Getchar()
{
	char c;
	while( (LPC_UART0->LSR & LSR_RDR) == 0 );  // Nothing received so just block
	c = LPC_UART0->RBR; // Read Receiver buffer register
	return c;
}

//Read from UART without blocking
//Returns
//The character received as an int or -1 if not character has been received.
int UART0_Getchar_NonBlocking()
{
	if( (LPC_UART0->LSR & LSR_RDR) == 0 ) {
		return -1;
	}
	return LPC_UART0->RBR;;					   // Read Receiver buffer register
}

int UART0_isDataAvailable() {
	return (LPC_UART0->LSR & LSR_RDR);
}

// ***********************
// Function to prints the string out over the UART
void UART0_PrintString(char *pcString)
{
	int i = 0;
	// loop through until reach string's zero terminator
	while (pcString[i] != 0) {
		UART0_Sendchar(pcString[i]); // print each character
		i++;
	}
}
/*********************** End UART 0 functions *********************************/


/*********************** Start UART 1 functions *******************************/
/*
 * Init Uart0
 * P0.15 = TXD
 * p0.16 = RXD
 *
 * The serial port is set to 8 data bits, 1 stop bit, no parity. I thought about
 * the ability to set these through this function but decided not to until it was
 * needed in order to keep the interface as simple as possible. No need to add
 * complexity that is not required.
 *
 * Return -1 on error, 0 on success.
 */
int initUart1(int baudRate) {
	int 	pclk;
	int 	dlEest;
	float 	divAddVal, mulVal;

	// PCLK_UART0 is being set = SystemCoreClock
#ifdef __V2__
	pclk = SystemCoreClock;
#endif
#ifndef __V2__
	pclk = SystemFrequency;
#endif

	//Get the correct fractional values for the given pclk and required baud rate
	if( getFractionValues(pclk, baudRate, &dlEest, &divAddVal, &mulVal) == -1 ) {
		return -1;
	}

	// Turn on power to UART1
	LPC_SC->PCONP |=  PCUART1_POWERON;

	// Turn on UART1 peripheral clock
	LPC_SC->PCLKSEL0 &= ~(PCLK_UART1_MASK);
	LPC_SC->PCLKSEL0 |=  (1 << PCLK_UART1);     // PCLK_periph = CCLK

	// Set PINSEL0 so that P0.15 = TXD1
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 30);
	LPC_PINCON->PINSEL0 |= ( 1L << 30);
	// Set PINSEL0 so that P0.16 = RXD1
	LPC_PINCON->PINSEL1 &= ~( 0x3 << 0);
	LPC_PINCON->PINSEL1 |= ( 1L << 0);
	// Set PINSEL0 so that P0.17 = CTS1
	LPC_PINCON->PINSEL1 &= ~( 0x3 << 2);
	LPC_PINCON->PINSEL1 |= ( 1L << 2);
	// Set PINSEL0 so that P0.22 = RTS1
	LPC_PINCON->PINSEL1 &= ~( 0x3 << 12);
	LPC_PINCON->PINSEL1 |= ( 1L << 12);

	LPC_UART1->LCR = 0x83;		// 8 bits, no Parity, 1 Stop bit, DLAB=1
	//LPC_UART1->LCR = 0x80 | 0x03 | 0x18 | 0x00;  // lcr_d Data bits, lcr_p Parity,   lcr_s Stop bit
	LPC_UART1->DLM = dlEest / 256;
	LPC_UART1->DLL = dlEest % 256;
	//Setup the fractional divider register
	LPC_UART1->FDR = (((int)mulVal)<<4)|(int)divAddVal;
	//LPC_UART1->LCR = 0x03;		// 8 bits, no Parity, 1 Stop bit DLAB = 0
	LPC_UART1->LCR = 0x00 | 0x03 | 0x18 | 0x00;  // lcr_d, lcr_p, lcr_s, DLAB = 0
	LPC_UART1->FCR = 0x07;		// Enable and reset TX and RX FIFO

	LPC_UART1->IER = 0x03;                          // Enable TX/RX interrupts

	//Debug code
	//Calc actual baud rate achieved
	//int uartBaudRate = pclk/( 16*dlEest*(1+(divAddVal/mulVal)) );
	//printf("\ndlEest         =%d\n\rSystemCoreClock=%d\nuartBaudRate=%d\n\rpclk=%d\n\r",dlEest,SystemCoreClock,uartBaudRate,pclk);

	uart1_etat = 0xc4;
	return 0;
}


int UART1_SetBaud( unsigned char baudrate)
{
	int debit;
	int 	pclk;
	int 	dlEest;
	float 	divAddVal, mulVal;
#ifdef __V2__
	pclk = SystemCoreClock;
#endif
#ifndef __V2__
	pclk = SystemFrequency;
#endif
	switch(baudrate)
	{
	case UART1_9600:
		debit = 9600;
		uart1_etat &= ~(0x7);
		break;
	case UART1_19200:
		uart1_etat &= ~(0x7);
		uart1_etat |= (0x1);
		debit = 19200;
		break;
	case UART1_38400:
		uart1_etat &= ~(0x7);
		uart1_etat |= (0x2);
		debit = 38400;
		break;
	case UART1_57600:
		uart1_etat &= ~(0x7);
		uart1_etat |= (0x3);
		debit = 57600;
		break;
	case UART1_115200:
		uart1_etat &= ~(0x7);
		uart1_etat |= (0x4);
		debit = 115200;
		break;
	}
	if( getFractionValues(pclk, debit, &dlEest, &divAddVal, &mulVal) == -1 )
	{
		return -1;
	}
	unsigned long lcr = LPC_UART1->LCR;
	LPC_UART1->LCR = 0x83;
	LPC_UART1->DLM = dlEest / 256;
	LPC_UART1->DLL = dlEest % 256;
	LPC_UART1->FDR = (((int)mulVal)<<4)|(int)divAddVal;
	LPC_UART1->LCR = lcr;
	LPC_UART1->FCR = 0x07;		// Enable and reset TX and RX FIFO
	return 0;
}

void UART1_SetParity( unsigned char parity)
{
	switch (parity)
	{
	case UART1_NONE:
		uart1_etat &= ~(0x3 << 4);
		LPC_UART1->LCR &= ~(1<<3);
		break;
	case UART1_EVEN:
		uart1_etat &= ~(0x3 << 4);
		uart1_etat |= (0x1 << 4);
		LPC_UART1->LCR &= ~(1<<5);
		LPC_UART1->LCR |= (1<<4);
		LPC_UART1->LCR |= (1<<3);
		break;
	case UART1_ODD:
		uart1_etat &= ~(0x3 << 4);
		uart1_etat |= (0x2 << 4);
		LPC_UART1->LCR &= ~(1<<5);
		LPC_UART1->LCR &= ~(1<<4);
		LPC_UART1->LCR |= (1<<3);
		break;
	}
}

void UART1_SetStop( unsigned char stop)
{
	switch( stop )
	{
	case UART1_STOP1:
		uart1_etat &= ~(1 << 3);
		LPC_UART1->LCR &= ~(1<<2);
		break;
	case UART1_STOP2:
		uart1_etat |= (1 << 3);
		LPC_UART1->LCR |= (1<<2);
		break;
	}
}

void UART1_SetLenght( unsigned char lenght)
{
	switch( lenght )
	{
	case UART1_LENGHT_5:
		uart1_etat &= ~(0x3 << 6);
		LPC_UART1->LCR &= ~(1<<0);
		LPC_UART1->LCR &= ~(1<<1);
		break;
	case UART1_LENGHT_6:
		uart1_etat &= ~(0x3 << 6);
		uart1_etat |= (0x1 << 6);
		LPC_UART1->LCR |= (1<<0);
		LPC_UART1->LCR &= ~(1<<1);
		break;
	case UART1_LENGHT_7:
		uart1_etat &= ~(0x3 << 6);
		uart1_etat |= (0x2 << 6);
		LPC_UART1->LCR &= ~(1<<0);
		LPC_UART1->LCR |= (1<<1);
		break;
	case UART1_LENGHT_8:
		uart1_etat |= (0x3 << 6);
		LPC_UART1->LCR |= (1<<0);
		LPC_UART1->LCR |= (1<<1);
		break;
	}
}

// ***********************
// Function to send character over UART
void UART1_Sendchar(char c)
{
	while( (LPC_UART1->LSR & LSR_THRE) == 0 );	// Block until tx empty

	LPC_UART1->THR = c;
}

// ***********************
// Function to get character from UART
char UART1_Getchar()
{
	char c;
	while( (LPC_UART1->LSR & LSR_RDR) == 0 );  // Nothing received so just block
	c = LPC_UART1->RBR; // Read Receiver buffer register
	return c;
}

//Read from UART without blocking
//Returns
//The character received as an int or -1 if not character has been received.
int UART1_Getchar_NonBlocking()
{
	if( (LPC_UART1->LSR & LSR_RDR) == 0 ) {
		return -1;
	}
	return LPC_UART1->RBR;;					   // Read Receiver buffer register
}

int UART1_isDataAvailable() {
	return (LPC_UART1->LSR & LSR_RDR);
}

// ***********************
// Function to prints the string out over the UART
void UART1_PrintString(char *pcString)
{
	int i = 0;
	// loop through until reach string's zero terminator
	while (pcString[i] != 0) {
		UART1_Sendchar(pcString[i]); // print each character
		i++;
	}
}
/*********************** End UART 1 functions *********************************/

/*********************** Start UART 2 functions *******************************/
/*
 * Init Uart2
 * P0.10 = TXD
 * p0.11 = RXD
 *
 * The serial port is set to 8 data bits, 1 stop bit, no parity. I thought about
 * the ability to set these through this function but decided not to until it was
 * needed in order to keep the interface as simple as possible. No need to add
 * complexity that is not required.
 *
 * Return -1 on error, 0 on success.
 */
int initUart2(int baudRate) {
	int 	pclk;
	int 	dlEest;
	float 	divAddVal, mulVal;

	// PCLK_UART2 is being set = SystemCoreClock
#ifdef __V2__
	pclk = SystemCoreClock;
#endif
#ifndef __V2__
	pclk = SystemFrequency;
#endif

	//Get the correct fractional values for the given pclk and required baud rate
	if( getFractionValues(pclk, baudRate, &dlEest, &divAddVal, &mulVal) == -1 ) {
		return -1;
	}

	// Turn on power to UART2
	LPC_SC->PCONP |=  PCUART2_POWERON;

	// Turn on UART2 peripheral clock
	LPC_SC->PCLKSEL1 &= ~(PCLK_UART2_MASK);
	LPC_SC->PCLKSEL1 |=  (1 << PCLK_UART2);     // PCLK_periph = CCLK

	// Set PINSEL0 so that P0.10 = TXD2
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 20);
	LPC_PINCON->PINSEL0 |= ( 1L << 20);
	// Set PINSEL0 so that P0.11 = RXD2
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 22);
	LPC_PINCON->PINSEL0 |= ( 1L << 22);

	//LPC_UART2->LCR = 0x83;		// 8 bits, no Parity, 1 Stop bit, DLAB=1
	LPC_UART2->LCR = 0x80 | 0x03 | 0x18 | 0x00;  // lcr_d Data bits, lcr_p Parity,   lcr_s Stop bit
	LPC_UART2->DLM = dlEest / 256;
	LPC_UART2->DLL = dlEest % 256;
	//Setup the fractional divider register
	LPC_UART2->FDR = (((int)mulVal)<<4)|(int)divAddVal;
	//LPC_UART2->LCR = 0x03;		// 8 bits, no Parity, 1 Stop bit DLAB = 0
	LPC_UART2->FCR = 0x07;		// Enable and reset TX and RX FIFO

	LPC_UART2->IER = 0x03;                          // Enable TX/RX interrupts


	//Debug code
	//Calc actual baud rate achieved
	//int uartBaudRate = pclk/( 16*dlEest*(1+(divAddVal/mulVal)) );
	//printf("\ndlEest         =%d\n\rSystemCoreClock=%d\nuartBaudRate=%d\n\rpclk=%d\n\r",dlEest,SystemCoreClock,uartBaudRate,pclk);

	return 0;
}

// ***********************
// Function to send character over UART
void UART2_Sendchar(char c)
{
	while( (LPC_UART2->LSR & LSR_THRE) == 0 );	// Block until tx empty

	LPC_UART2->THR = c;
}

// ***********************
// Function to get character from UART
char UART2_Getchar()
{
	char c;
	while( (LPC_UART2->LSR & LSR_RDR) == 0 );  // Nothing received so just block
	c = LPC_UART2->RBR; // Read Receiver buffer register
	return c;
}

//Read from UART without blocking
//Returns
//The character received as an int or -1 if not character has been received.
int UART2_Getchar_NonBlocking()
{
	if( (LPC_UART2->LSR & LSR_RDR) == 0 ) {
		return -1;
	}
	return LPC_UART2->RBR;;					   // Read Receiver buffer register
}

int UART2_isDataAvailable() {
	return (LPC_UART2->LSR & LSR_RDR);
}

// ***********************
// Function to prints the string out over the UART
void UART2_PrintString(char *pcString)
{
	int i = 0;
	// loop through until reach string's zero terminator
	while (pcString[i] != 0) {
		UART2_Sendchar(pcString[i]); // print each character
		i++;
	}
}
/*********************** End UART 2 functions *********************************/


/*********************** Start UART 3 functions *******************************/
/*
 * Init Uart3
 * P0.0 = TXD
 * p0.1 = RXD
 *
 * The serial port is set to 8 data bits, 1 stop bit, no parity. I thought about
 * the ability to set these through this function but decided not to until it was
 * needed in order to keep the interface as simple as possible. No need to add
 * complexity that is not required.
 *
 * Return -1 on error, 0 on success.
 */
int initUart3(int baudRate) {
	int 	pclk;
	int 	dlEest;
	float 	divAddVal, mulVal;

	// PCLK_UART3 is being set = SystemCoreClock
#ifdef __V2__
	pclk = SystemCoreClock;
#endif
#ifndef __V2__
	pclk = SystemFrequency;
#endif

	//Get the correct fractional values for the given pclk and required baud rate
	if( getFractionValues(pclk, baudRate, &dlEest, &divAddVal, &mulVal) == -1 ) {
		return -1;
	}

	// Turn on power to UART3
	LPC_SC->PCONP |=  PCUART3_POWERON;

	// Turn on UART3 peripheral clock
	LPC_SC->PCLKSEL1 &= ~(PCLK_UART3_MASK);
	LPC_SC->PCLKSEL1 |=  (1 << PCLK_UART3);     // PCLK_periph = CCLK

#ifndef __JEREM__
	// Set PINSEL0 so that P4.28 = TXD3
	LPC_PINCON->PINSEL9 |= ( 0x3 << 24);
	// Set PINSEL0 so that P4.29 = RXD3
	LPC_PINCON->PINSEL9 |= ( 0x3 << 26);
#endif
#ifdef __JEREM__
	// Set PINSEL0 so that P4.28 = TXD3
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 0);
	LPC_PINCON->PINSEL0 |= ( 0x2 << 0);
	// Set PINSEL0 so that P4.29 = RXD3
	LPC_PINCON->PINSEL0 &= ~( 0x3 << 2);
	LPC_PINCON->PINSEL0 |= ( 0x2 << 2);
#endif

	LPC_UART3->LCR = 0x83;		// 8 bits, no Parity, 1 Stop bit, DLAB=1
	LPC_UART3->DLM = dlEest / 256;
	LPC_UART3->DLL = dlEest % 256;
	//Setup the fractional divider register
	LPC_UART3->FDR = (((int)mulVal)<<4)|(int)divAddVal;
	LPC_UART3->LCR = 0x03;		// 8 bits, no Parity, 1 Stop bit DLAB = 0
	LPC_UART3->FCR = 0x07;		// Enable and reset TX and RX FIFO

	LPC_UART3->IER = 0x03;                          // Enable TX/RX interrupts

	//Debug code
	//Calc actual baud rate achieved
	//int uartBaudRate = pclk/( 16*dlEest*(1+(divAddVal/mulVal)) );
	//printf("\ndlEest         =%d\n\rSystemCoreClock=%d\nuartBaudRate=%d\n\rpclk=%d\n\r",dlEest,SystemCoreClock,uartBaudRate,pclk);

	return 0;
}

// ***********************
// Function to send character over UART
void UART3_Sendchar(char c)
{
	while( (LPC_UART3->LSR & LSR_THRE) == 0 );	// Block until tx empty

	LPC_UART3->THR = c;
}

// ***********************
// Function to get character from UART
char UART3_Getchar()
{
	char c;
	while( (LPC_UART3->LSR & LSR_RDR) == 0 );  // Nothing received so just block
	c = LPC_UART3->RBR; // Read Receiver buffer register
	return c;
}

//Read from UART without blocking
//Returns
//The character received as an int or -1 if not character has been received.
int UART3_Getchar_NonBlocking()
{
	if( (LPC_UART3->LSR & LSR_RDR) == 0 ) {
		return -1;
	}
	return LPC_UART3->RBR;;					   // Read Receiver buffer register
}

int UART3_isDataAvailable() {
	return (LPC_UART3->LSR & LSR_RDR);
}

// ***********************
// Function to prints the string out over the UART
void UART3_PrintString(char *pcString)
{
	int i = 0;
	// loop through until reach string's zero terminator
	while (pcString[i] != 0) {
		UART3_Sendchar(pcString[i]); // print each character
		i++;
	}
}
/*********************** End UART 3 functions *********************************/


/*********************** Start Generic UART functions *******************************/
/*
 * Init Uart3
 * P0.0 = TXD
 * p0.1 = RXD
 *
 * uart = 0,1,2,3 for LPC1768 target for all these uart functions.
 *
 * baudRate = The required Bps
 *
 * The serial port is set to 8 data bits, 1 stop bit, no parity. I thought about
 * the ability to set these through this function but decided not to until it was
 * needed in order to keep the interface as simple as possible. No need to add
 * complexity that is not required.
 *
 * Return -1 on error, 0 on success.
 */
int initUart(int uart, int baudRate) {
	int rc=-1;
	if( uart == 0 ) {
		rc = initUart0(baudRate);
	}
	else if( uart == 1 ) {
		rc = initUart1(baudRate);
	}
	else if( uart == 2 ) {
		rc = initUart2(baudRate);
	}
	else if( uart == 3 ) {
		rc = initUart3(baudRate);
	}
	return rc;
}

// ***********************
// Function to send character over UART
int UART_Sendchar(int uart, char c)
{
	int rc=-1;
	if( uart == 0 ) {
		UART0_Sendchar(c);
		rc=0;
	}
	else if( uart == 1 ) {
		UART1_Sendchar(c);
		rc=0;
	}
	else if( uart == 2 ) {
		UART2_Sendchar(c);
		rc=0;
	}
	else if( uart == 3 ) {
		UART3_Sendchar(c);
		rc=0;
	}
	return rc;
}

// ***********************
// Function to get character from UART
char UART_Getchar(int uart)
{
	char c=0;
	if( uart == 0 ) {
		c = UART0_Getchar(c);
	}
	else if( uart == 1 ) {
		c = UART1_Getchar(c);
	}
	else if( uart == 2 ) {
		c = UART2_Getchar(c);
	}
	else if( uart == 3 ) {
		c = UART3_Getchar(c);
	}
	return c;
}

//Read from UART without blocking
//Returns
//The character received or -1 if no character is available to be read.
int UART_Getchar_NonBlocking(int uart)
{
	int i=-1;
	if( uart == 0 ) {
		i = UART0_Getchar_NonBlocking();
	}
	else if( uart == 1 ) {
		i = UART1_Getchar_NonBlocking();
	}
	else if( uart == 2 ) {
		i = UART2_Getchar_NonBlocking();
	}
	else if( uart == 3 ) {
		i = UART3_Getchar_NonBlocking();
	}
	return i;
}

//Check if uart RX data is available
//Return 1 if RX data is available, 0 if not, -1 if uart is not 0-3.
int UART_isDataAvailable(int uart) {
	int a=-1;
	if( uart == 0 ) {
		a = UART0_isDataAvailable();
	}
	else if( uart == 1 ) {
		a = UART1_isDataAvailable();
	}
	else if( uart == 2 ) {
		a = UART2_isDataAvailable();
	}
	else if( uart == 3 ) {
		a = UART3_isDataAvailable();
	}
	return a;
}

// ***********************
// Function to prints the string out over the UART
int UART_PrintString(int uart, char *pcString)
{
	int i = 0;
	int rc=-1;

	// loop through until reach string's zero terminator
	while (pcString[i] != 0) {
		if( uart == 0 ) {
			UART0_Sendchar(pcString[i]);
			rc=0;
		}
		else if( uart == 1 ) {
			UART1_Sendchar(pcString[i]);
			rc=0;
		}
		else if( uart == 2 ) {
			UART2_Sendchar(pcString[i]);
			rc=0;
		}
		else if( uart == 3 ) {
			UART3_Sendchar(pcString[i]);
			rc=0;
		}
		i++;
	}
	return rc;
}

/*********************** End Generic UART functions *********************************/
