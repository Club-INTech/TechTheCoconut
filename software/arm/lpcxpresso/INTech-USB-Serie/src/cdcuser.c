/*----------------------------------------------------------------------------
 *      U S B  -  K e r n e l
 *----------------------------------------------------------------------------
 *      Name:    cdcuser.c
 *      Purpose: USB Communication Device Class User module 
 *      Version: V1.10
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

#include "type.h"

#include "usb.h"
#include "usbhw.h"
#include "usbcfg.h"
#include "usbcore.h"
#include "cdc.h"
#include "cdcuser.h"
#include "serial.h"


unsigned char BulkBufIn0  [USB_CDC_BUFSIZE];            // Buffer to store USB IN  packet
unsigned char BulkBufOut0 [USB_CDC_BUFSIZE];            // Buffer to store USB OUT packet

unsigned char BulkBufIn1  [USB_CDC_BUFSIZE];            // Buffer to store USB IN  packet
unsigned char BulkBufOut1 [USB_CDC_BUFSIZE];            // Buffer to store USB OUT packet

unsigned char BulkBufIn2  [USB_CDC_BUFSIZE];            // Buffer to store USB IN  packet
unsigned char BulkBufOut2 [USB_CDC_BUFSIZE];            // Buffer to store USB OUT packet

unsigned char BulkBufIn3  [USB_CDC_BUFSIZE];            // Buffer to store USB IN  packet
unsigned char BulkBufOut3 [USB_CDC_BUFSIZE];            // Buffer to store USB OUT packet

unsigned char BulkBufIn4  [USB_CDC_BUFSIZE];            // Buffer to store USB IN  packet
unsigned char BulkBufOut4 [USB_CDC_BUFSIZE];            // Buffer to store USB OUT packet

unsigned char NotificationBuf [10];

//CDC_LINE_CODING CDC_LineCoding  = {9600, 0, 0, 8};
CDC_LINE_CODING CDC_LineCoding  = {115200, 0, 0, 8};	// 115200 baudrate, 2 bCharFormat,  EVEN bParityType, 8 bDataBits

unsigned short  CDC0_SerialState = 0x0000;
unsigned short  CDC0_DepInEmpty  = 1;                   // Data IN EP is empty

unsigned short  CDC1_SerialState = 0x0000;
unsigned short  CDC1_DepInEmpty  = 1;                   // Data IN EP is empty

unsigned short  CDC2_SerialState = 0x0000;
unsigned short  CDC2_DepInEmpty  = 1;                   // Data IN EP is empty

unsigned short  CDC3_SerialState = 0x0000;
unsigned short  CDC3_DepInEmpty  = 1;                   // Data IN EP is empty

/*----------------------------------------------------------------------------
  We need a buffer for incomming data on USB port because USB receives
  much faster than  UART transmits
 *---------------------------------------------------------------------------*/
/* Buffer masks */
#define CDC_BUF_SIZE               (64)               // Output buffer in bytes (power 2)
                                                       // large enough for file transfer
#define CDC_BUF_MASK               (CDC_BUF_SIZE-1ul)

/* Buffer read / write macros */
#define CDC_BUF_RESET(cdcBuf)      (cdcBuf.rdIdx = cdcBuf.wrIdx = 0)
#define CDC_BUF_WR(cdcBuf, dataIn) (cdcBuf.data[CDC_BUF_MASK & cdcBuf.wrIdx++] = (dataIn))
#define CDC_BUF_RD(cdcBuf)         (cdcBuf.data[CDC_BUF_MASK & cdcBuf.rdIdx++])   
#define CDC_BUF_EMPTY(cdcBuf)      (cdcBuf.rdIdx == cdcBuf.wrIdx)
#define CDC_BUF_FULL(cdcBuf)       (cdcBuf.rdIdx == cdcBuf.wrIdx+1)
#define CDC_BUF_COUNT(cdcBuf)      (CDC_BUF_MASK & (cdcBuf.wrIdx - cdcBuf.rdIdx))


// CDC output buffer
typedef struct __CDC_BUF_T {
  unsigned char data[CDC_BUF_SIZE];
  unsigned int wrIdx;
  unsigned int rdIdx;
} CDC_BUF_T;

CDC_BUF_T  CDC0_OutBuf;                                 // buffer for all CDC Out data
CDC_BUF_T  CDC1_OutBuf;                                 // buffer for all CDC Out data
CDC_BUF_T  CDC2_OutBuf;                                 // buffer for all CDC Out data
CDC_BUF_T  CDC3_OutBuf;                                 // buffer for all CDC Out data
CDC_BUF_T  CDC4_OutBuf;                                 // buffer for all CDC Out data

/*----------------------------------------------------------------------------
  read data from CDC_OutBuf
 *---------------------------------------------------------------------------*/
int CDC0_RdOutBuf (char *buffer, const int *length) {
  int bytesToRead, bytesRead;
  
  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;


  // ... add code to check for underrun

  while (bytesToRead--) {
    *buffer++ = CDC_BUF_RD(CDC0_OutBuf);
  }
  return (bytesRead);  
}

int CDC1_RdOutBuf (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;


  // ... add code to check for underrun

  while (bytesToRead--) {
    *buffer++ = CDC_BUF_RD(CDC1_OutBuf);
  }
  return (bytesRead);
}

int CDC2_RdOutBuf (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;


  // ... add code to check for underrun

  while (bytesToRead--) {
    *buffer++ = CDC_BUF_RD(CDC2_OutBuf);
  }
  return (bytesRead);
}

int CDC3_RdOutBuf (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;


  // ... add code to check for underrun

  while (bytesToRead--) {
    *buffer++ = CDC_BUF_RD(CDC3_OutBuf);
  }
  return (bytesRead);
}

int CDC4_RdOutBuf (char *buffer, const int *length) {
  int bytesToRead, bytesRead;

  /* Read *length bytes, block if *bytes are not avaialable	*/
  bytesToRead = *length;
  bytesToRead = (bytesToRead < (*length)) ? bytesToRead : (*length);
  bytesRead = bytesToRead;


  // ... add code to check for underrun

  while (bytesToRead--) {
    *buffer++ = CDC_BUF_RD(CDC4_OutBuf);
  }
  return (bytesRead);
}

/*----------------------------------------------------------------------------
  write data to CDC_OutBuf
 *---------------------------------------------------------------------------*/
int CDC0_WrOutBuf (const char *buffer, int *length) {
  int bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;


  // ... add code to check for overwrite

  while (bytesToWrite) {
      CDC_BUF_WR(CDC0_OutBuf, *buffer++);           // Copy Data to buffer
      bytesToWrite--;
  }     

  return (bytesWritten); 
}

int CDC1_WrOutBuf (const char *buffer, int *length) {
  int bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;


  // ... add code to check for overwrite

  while (bytesToWrite) {
      CDC_BUF_WR(CDC1_OutBuf, *buffer++);           // Copy Data to buffer
      bytesToWrite--;
  }

  return (bytesWritten);
}

int CDC2_WrOutBuf (const char *buffer, int *length) {
  int bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;


  // ... add code to check for overwrite

  while (bytesToWrite) {
      CDC_BUF_WR(CDC2_OutBuf, *buffer++);           // Copy Data to buffer
      bytesToWrite--;
  }

  return (bytesWritten);
}

int CDC3_WrOutBuf (const char *buffer, int *length) {
  int bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;


  // ... add code to check for overwrite

  while (bytesToWrite) {
      CDC_BUF_WR(CDC3_OutBuf, *buffer++);           // Copy Data to buffer
      bytesToWrite--;
  }

  return (bytesWritten);
}

int CDC4_WrOutBuf (const char *buffer, int *length) {
  int bytesToWrite, bytesWritten;

  // Write *length bytes
  bytesToWrite = *length;
  bytesWritten = bytesToWrite;


  // ... add code to check for overwrite

  while (bytesToWrite) {
      CDC_BUF_WR(CDC4_OutBuf, *buffer++);           // Copy Data to buffer
      bytesToWrite--;
  }

  return (bytesWritten);
}

/*----------------------------------------------------------------------------
  check if character(s) are available at CDC_OutBuf
 *---------------------------------------------------------------------------*/
int CDC0_OutBufAvailChar (int *availChar) {

  *availChar = CDC_BUF_COUNT(CDC0_OutBuf);

  return (0);
}

int CDC1_OutBufAvailChar (int *availChar) {

  *availChar = CDC_BUF_COUNT(CDC1_OutBuf);

  return (0);
}

int CDC2_OutBufAvailChar (int *availChar) {

  *availChar = CDC_BUF_COUNT(CDC2_OutBuf);

  return (0);
}

int CDC3_OutBufAvailChar (int *availChar) {

  *availChar = CDC_BUF_COUNT(CDC3_OutBuf);

  return (0);
}

int CDC4_OutBufAvailChar (int *availChar) {

  *availChar = CDC_BUF_COUNT(CDC4_OutBuf);

  return (0);
}
/* end Buffer handling */


/*----------------------------------------------------------------------------
  CDC Initialisation
  Initializes the data structures and serial port
  Parameters:   None 
  Return Value: None
 *---------------------------------------------------------------------------*/
void CDC_Init (char portNum ) {

	ser_OpenPort (portNum);
	if ( portNum == 0 )
	{
		CDC_BUF_RESET(CDC0_OutBuf);
		CDC0_DepInEmpty  = 1;
		CDC0_SerialState = CDC0_GetSerialState();
	}
	else if ( portNum == 1 )
	{
		CDC_BUF_RESET(CDC1_OutBuf);
		CDC1_DepInEmpty  = 1;
		CDC1_SerialState = CDC1_GetSerialState();
	}
	else if ( portNum == 2 )
	{
		CDC_BUF_RESET(CDC2_OutBuf);
		CDC2_DepInEmpty  = 1;
		CDC2_SerialState = CDC2_GetSerialState();
	}
	else if ( portNum == 3 )
	{
		CDC_BUF_RESET(CDC3_OutBuf);
		CDC3_DepInEmpty  = 1;
		CDC3_SerialState = CDC3_GetSerialState();
	}

	CDC_BUF_RESET(CDC4_OutBuf);
}


/*----------------------------------------------------------------------------
  CDC SendEncapsulatedCommand Request Callback
  Called automatically on CDC SEND_ENCAPSULATED_COMMAND Request
  Parameters:   None                          (global SetupPacket and EP0Buf)
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_SendEncapsulatedCommand (void) {

  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC GetEncapsulatedResponse Request Callback
  Called automatically on CDC Get_ENCAPSULATED_RESPONSE Request
  Parameters:   None                          (global SetupPacket and EP0Buf)
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_GetEncapsulatedResponse (void) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC SetCommFeature Request Callback
  Called automatically on CDC Set_COMM_FATURE Request
  Parameters:   FeatureSelector
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_SetCommFeature (unsigned short wFeatureSelector) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC GetCommFeature Request Callback
  Called automatically on CDC Get_COMM_FATURE Request
  Parameters:   FeatureSelector
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_GetCommFeature (unsigned short wFeatureSelector) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC ClearCommFeature Request Callback
  Called automatically on CDC CLEAR_COMM_FATURE Request
  Parameters:   FeatureSelector
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_ClearCommFeature (unsigned short wFeatureSelector) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC SetLineCoding Request Callback
  Called automatically on CDC SET_LINE_CODING Request
  Parameters:   none                    (global SetupPacket and EP0Buf)
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_SetLineCoding (void) {

//  CDC_LineCoding.dwDTERate   =   (EP0Buf[0] <<  0)
//                               | (EP0Buf[1] <<  8)
//                               | (EP0Buf[2] << 16)
//                               | (EP0Buf[3] << 24);
//  CDC_LineCoding.bCharFormat =  EP0Buf[4];
//  CDC_LineCoding.bParityType =  EP0Buf[5];
//  CDC_LineCoding.bDataBits   =  EP0Buf[6];
//
//#if PORT_NUM
//  ser_ClosePort(1);
//  ser_OpenPort (1);
//  ser_InitPort1 (CDC_LineCoding.dwDTERate,
//                CDC_LineCoding.bDataBits,
//                CDC_LineCoding.bParityType,
//                CDC_LineCoding.bCharFormat);
//#else
//  ser_ClosePort(0);
//  ser_OpenPort (0);
//  ser_InitPort0 (CDC_LineCoding.dwDTERate,
//                CDC_LineCoding.bDataBits,
//                CDC_LineCoding.bParityType,
//                CDC_LineCoding.bCharFormat);
//#endif
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC GetLineCoding Request Callback
  Called automatically on CDC GET_LINE_CODING Request
  Parameters:   None                         (global SetupPacket and EP0Buf)
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_GetLineCoding (void) {

  EP0Buf[0] = (CDC_LineCoding.dwDTERate >>  0) & 0xFF;
  EP0Buf[1] = (CDC_LineCoding.dwDTERate >>  8) & 0xFF;
  EP0Buf[2] = (CDC_LineCoding.dwDTERate >> 16) & 0xFF;
  EP0Buf[3] = (CDC_LineCoding.dwDTERate >> 24) & 0xFF;
  EP0Buf[4] =  CDC_LineCoding.bCharFormat;
  EP0Buf[5] =  CDC_LineCoding.bParityType;
  EP0Buf[6] =  CDC_LineCoding.bDataBits;

  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC SetControlLineState Request Callback
  Called automatically on CDC SET_CONTROL_LINE_STATE Request
  Parameters:   ControlSignalBitmap 
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_SetControlLineState (unsigned short wControlSignalBitmap) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC SendBreak Request Callback
  Called automatically on CDC Set_COMM_FATURE Request
  Parameters:   0xFFFF  start of Break 
                0x0000  stop  of Break
                0x####  Duration of Break
  Return Value: TRUE - Success, FALSE - Error
 *---------------------------------------------------------------------------*/
uint32_t CDC_SendBreak (unsigned short wDurationOfBreak) {

  /* ... add code to handle request */
  return (TRUE);
}


/*----------------------------------------------------------------------------
  CDC_BulkIn call on DataIn Request
  Parameters:   none
  Return Value: none
 *---------------------------------------------------------------------------*/
void CDC0_BulkIn(void) {
  int numBytesRead, numBytesAvail;
	
  ser0_AvailChar (&numBytesAvail);

  // ... add code to check for overwrite

  numBytesRead = ser0_Read ((char *)&BulkBufIn0[0], &numBytesAvail);

  // send over USB
  if (numBytesRead > 0) {
	USB_WriteEP (CDC0_DEP_IN, &BulkBufIn0[0], numBytesRead);
  }
  else {
    CDC0_DepInEmpty = 1;
  }
}

void CDC1_BulkIn(void) {
  int numBytesRead, numBytesAvail;

  ser1_AvailChar (&numBytesAvail);

  // ... add code to check for overwrite

  numBytesRead = ser1_Read ((char *)&BulkBufIn1[0], &numBytesAvail);

  // send over USB
  if (numBytesRead > 0) {
	USB_WriteEP (CDC1_DEP_IN, &BulkBufIn1[0], numBytesRead);
  }
  else {
    CDC1_DepInEmpty = 1;
  }
}

void CDC2_BulkIn(void) {
  int numBytesRead, numBytesAvail;

  ser2_AvailChar (&numBytesAvail);

  // ... add code to check for overwrite

  numBytesRead = ser2_Read ((char *)&BulkBufIn2[0], &numBytesAvail);

  // send over USB
  if (numBytesRead > 0) {
	USB_WriteEP (CDC2_DEP_IN, &BulkBufIn2[0], numBytesRead);
  }
  else {
    CDC2_DepInEmpty = 1;
  }
}

void CDC3_BulkIn(void) {
  int numBytesRead, numBytesAvail;

  ser3_AvailChar (&numBytesAvail);

  // ... add code to check for overwrite

  numBytesRead = ser3_Read ((char *)&BulkBufIn3[0], &numBytesAvail);

  // send over USB
  if (numBytesRead > 0) {
	USB_WriteEP (CDC3_DEP_IN, &BulkBufIn3[0], numBytesRead);
  }
  else {
    CDC3_DepInEmpty = 1;
  }
} 


/*----------------------------------------------------------------------------
  CDC_BulkOut call on DataOut Request
  Parameters:   none
  Return Value: none
 *---------------------------------------------------------------------------*/
void CDC0_BulkOut(void) {
  int numBytesRead;

  // get data from USB into intermediate buffer
  numBytesRead = USB_ReadEP(CDC0_DEP_OUT, &BulkBufOut0[0]);

  // ... add code to check for overwrite

  // store data in a buffer to transmit it over serial interface
  CDC0_WrOutBuf ((char *)&BulkBufOut0[0], &numBytesRead);

}

void CDC1_BulkOut(void) {
  int numBytesRead;

  // get data from USB into intermediate buffer
  numBytesRead = USB_ReadEP(CDC1_DEP_OUT, &BulkBufOut1[0]);

  // ... add code to check for overwrite

  // store data in a buffer to transmit it over serial interface
  CDC1_WrOutBuf ((char *)&BulkBufOut1[0], &numBytesRead);

}

void CDC2_BulkOut(void) {
  int numBytesRead;

  // get data from USB into intermediate buffer
  numBytesRead = USB_ReadEP(CDC2_DEP_OUT, &BulkBufOut2[0]);

  // ... add code to check for overwrite

  // store data in a buffer to transmit it over serial interface
  CDC2_WrOutBuf ((char *)&BulkBufOut2[0], &numBytesRead);

}

void CDC3_BulkOut(void) {
  int numBytesRead;

  // get data from USB into intermediate buffer
  numBytesRead = USB_ReadEP(CDC3_DEP_OUT, &BulkBufOut3[0]);

  // ... add code to check for overwrite

  // store data in a buffer to transmit it over serial interface
  CDC3_WrOutBuf ((char *)&BulkBufOut3[0], &numBytesRead);

}

void CDC4_BulkOut(void) {
  int numBytesRead;

  // get data from USB into intermediate buffer
  numBytesRead = USB_ReadEP(CDC4_DEP_OUT, &BulkBufOut4[0]);

  // ... add code to check for overwrite

  // store data in a buffer to transmit it over serial interface
  CDC4_WrOutBuf ((char *)&BulkBufOut4[0], &numBytesRead);

}


/*----------------------------------------------------------------------------
  Get the SERIAL_STATE as defined in usbcdc11.pdf, 6.3.5, Table 69.
  Parameters:   none
  Return Value: SerialState as defined in usbcdc11.pdf
 *---------------------------------------------------------------------------*/
unsigned short CDC0_GetSerialState (void) {
  unsigned short temp;

  CDC0_SerialState = 0;
  ser0_LineState (&temp);

  if (temp & 0x8000)  CDC0_SerialState |= CDC_SERIAL_STATE_RX_CARRIER;
  if (temp & 0x2000)  CDC0_SerialState |= CDC_SERIAL_STATE_TX_CARRIER;
  if (temp & 0x0010)  CDC0_SerialState |= CDC_SERIAL_STATE_BREAK;
  if (temp & 0x4000)  CDC0_SerialState |= CDC_SERIAL_STATE_RING;
  if (temp & 0x0008)  CDC0_SerialState |= CDC_SERIAL_STATE_FRAMING;
  if (temp & 0x0004)  CDC0_SerialState |= CDC_SERIAL_STATE_PARITY;
  if (temp & 0x0002)  CDC0_SerialState |= CDC_SERIAL_STATE_OVERRUN;

  return (CDC0_SerialState);
}

unsigned short CDC1_GetSerialState (void) {
  unsigned short temp;

  CDC1_SerialState = 0;
  ser1_LineState (&temp);

  if (temp & 0x8000)  CDC1_SerialState |= CDC_SERIAL_STATE_RX_CARRIER;
  if (temp & 0x2000)  CDC1_SerialState |= CDC_SERIAL_STATE_TX_CARRIER;
  if (temp & 0x0010)  CDC1_SerialState |= CDC_SERIAL_STATE_BREAK;
  if (temp & 0x4000)  CDC1_SerialState |= CDC_SERIAL_STATE_RING;
  if (temp & 0x0008)  CDC1_SerialState |= CDC_SERIAL_STATE_FRAMING;
  if (temp & 0x0004)  CDC1_SerialState |= CDC_SERIAL_STATE_PARITY;
  if (temp & 0x0002)  CDC1_SerialState |= CDC_SERIAL_STATE_OVERRUN;

  return (CDC1_SerialState);
}

unsigned short CDC2_GetSerialState (void) {
  unsigned short temp;

  CDC2_SerialState = 0;
  ser2_LineState (&temp);

  if (temp & 0x8000)  CDC2_SerialState |= CDC_SERIAL_STATE_RX_CARRIER;
  if (temp & 0x2000)  CDC2_SerialState |= CDC_SERIAL_STATE_TX_CARRIER;
  if (temp & 0x0010)  CDC2_SerialState |= CDC_SERIAL_STATE_BREAK;
  if (temp & 0x4000)  CDC2_SerialState |= CDC_SERIAL_STATE_RING;
  if (temp & 0x0008)  CDC2_SerialState |= CDC_SERIAL_STATE_FRAMING;
  if (temp & 0x0004)  CDC2_SerialState |= CDC_SERIAL_STATE_PARITY;
  if (temp & 0x0002)  CDC2_SerialState |= CDC_SERIAL_STATE_OVERRUN;

  return (CDC2_SerialState);
}

unsigned short CDC3_GetSerialState (void) {
  unsigned short temp;

  CDC3_SerialState = 0;
  ser3_LineState (&temp);

  if (temp & 0x8000)  CDC3_SerialState |= CDC_SERIAL_STATE_RX_CARRIER;
  if (temp & 0x2000)  CDC3_SerialState |= CDC_SERIAL_STATE_TX_CARRIER;
  if (temp & 0x0010)  CDC3_SerialState |= CDC_SERIAL_STATE_BREAK;
  if (temp & 0x4000)  CDC3_SerialState |= CDC_SERIAL_STATE_RING;
  if (temp & 0x0008)  CDC3_SerialState |= CDC_SERIAL_STATE_FRAMING;
  if (temp & 0x0004)  CDC3_SerialState |= CDC_SERIAL_STATE_PARITY;
  if (temp & 0x0002)  CDC3_SerialState |= CDC_SERIAL_STATE_OVERRUN;

  return (CDC3_SerialState);
}


/*----------------------------------------------------------------------------
  Send the SERIAL_STATE notification as defined in usbcdc11.pdf, 6.3.5.
 *---------------------------------------------------------------------------*/
void CDC0_NotificationIn (void) {

  NotificationBuf[0] = 0xA1;                           // bmRequestType
  NotificationBuf[1] = CDC_NOTIFICATION_SERIAL_STATE;  // bNotification (SERIAL_STATE)
  NotificationBuf[2] = 0x00;                           // wValue
  NotificationBuf[3] = 0x00;
  NotificationBuf[4] = 0x00;                           // wIndex (Interface #, LSB first)
  NotificationBuf[5] = 0x00;
  NotificationBuf[6] = 0x02;                           // wLength (Data length = 2 bytes, LSB first)
  NotificationBuf[7] = 0x00; 
  NotificationBuf[8] = (CDC0_SerialState >>  0) & 0xFF; // UART State Bitmap (16bits, LSB first)
  NotificationBuf[9] = (CDC0_SerialState >>  8) & 0xFF;

  USB_WriteEP (CDC0_CEP_IN, &NotificationBuf[0], 10);   // send notification
}

void CDC1_NotificationIn (void) {

  NotificationBuf[0] = 0xA1;                           // bmRequestType
  NotificationBuf[1] = CDC_NOTIFICATION_SERIAL_STATE;  // bNotification (SERIAL_STATE)
  NotificationBuf[2] = 0x00;                           // wValue
  NotificationBuf[3] = 0x00;
  NotificationBuf[4] = 0x00;                           // wIndex (Interface #, LSB first)
  NotificationBuf[5] = 0x00;
  NotificationBuf[6] = 0x02;                           // wLength (Data length = 2 bytes, LSB first)
  NotificationBuf[7] = 0x00;
  NotificationBuf[8] = (CDC1_SerialState >>  0) & 0xFF; // UART State Bitmap (16bits, LSB first)
  NotificationBuf[9] = (CDC1_SerialState >>  8) & 0xFF;

  USB_WriteEP (CDC1_CEP_IN, &NotificationBuf[0], 10);   // send notification
}
