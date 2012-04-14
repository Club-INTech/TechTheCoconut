/*----------------------------------------------------------------------------
 *      U S B  -  K e r n e l
 *----------------------------------------------------------------------------
 *      Name:    cdcuser.h
 *      Purpose: USB Communication Device Class User module Definitions
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

#ifndef __CDCUSER_H__
#define __CDCUSER_H__

/* CDC buffer handling */
extern int CDC0_RdOutBuf        (char *buffer, const int *length);
extern int CDC1_RdOutBuf        (char *buffer, const int *length);
extern int CDC1_RdOutBuf        (char *buffer, const int *length);
extern int CDC2_RdOutBuf        (char *buffer, const int *length);
extern int CDC3_RdOutBuf        (char *buffer, const int *length);
extern int CDC4_RdOutBuf        (char *buffer, const int *length);

extern int CDC0_WrOutBuf        (const char *buffer, int *length);
extern int CDC1_WrOutBuf        (const char *buffer, int *length);
extern int CDC2_WrOutBuf        (const char *buffer, int *length);
extern int CDC3_WrOutBuf        (const char *buffer, int *length);
extern int CDC4_WrOutBuf        (const char *buffer, int *length);

extern int CDC0_OutBufAvailChar (int *availChar);
extern int CDC1_OutBufAvailChar (int *availChar);
extern int CDC2_OutBufAvailChar (int *availChar);
extern int CDC3_OutBufAvailChar (int *availChar);
extern int CDC4_OutBufAvailChar (int *availChar);

/* CDC 0 Data In/Out Endpoint Address */
#define CDC0_DEP_IN       USB_ENDPOINT_IN(2)		// 0x82
#define CDC0_DEP_OUT      USB_ENDPOINT_OUT(2)		// 0x02

/* CDC 0 Communication In Endpoint Address */
#define CDC0_CEP_IN       USB_ENDPOINT_IN(1) 		// 0x81

/* CDC 1 Data In/Out Endpoint Address */
#define CDC1_DEP_IN       USB_ENDPOINT_IN(5)		// 0x85
#define CDC1_DEP_OUT      USB_ENDPOINT_OUT(5)		// 0x05

/* CDC 1 Communication In Endpoint Address */
#define CDC1_CEP_IN       USB_ENDPOINT_IN(4)		// 0x84

/* CDC 2 Data In/Out Endpoint Address */
#define CDC2_DEP_IN       USB_ENDPOINT_IN(8)		// 0x88
#define CDC2_DEP_OUT      USB_ENDPOINT_OUT(8)		// 0x08

/* CDC 2 Communication In Endpoint Address */
#define CDC2_CEP_IN       USB_ENDPOINT_IN(7)		// 0x87

/* CDC 3 Data In/Out Endpoint Address */
#define CDC3_DEP_IN       USB_ENDPOINT_IN(11)		// 0x8B
#define CDC3_DEP_OUT      USB_ENDPOINT_OUT(11)		// 0x0B

/* CDC 3 Communication In Endpoint Address */
#define CDC3_CEP_IN       USB_ENDPOINT_IN(10)		// 0x8A

/* CDC 4 Data In/Out Endpoint Address */
#define CDC4_DEP_IN       USB_ENDPOINT_IN(14)		// 0x8E
#define CDC4_DEP_OUT      USB_ENDPOINT_OUT(14)		// 0x0E

/* CDC 4 Communication In Endpoint Address */
#define CDC4_CEP_IN       USB_ENDPOINT_IN(13)		// 0x8D

/* CDC Requests Callback Functions */
extern uint32_t CDC_SendEncapsulatedCommand  (void);
extern uint32_t CDC_GetEncapsulatedResponse  (void);
extern uint32_t CDC_SetCommFeature           (unsigned short wFeatureSelector);
extern uint32_t CDC_GetCommFeature           (unsigned short wFeatureSelector);
extern uint32_t CDC_ClearCommFeature         (unsigned short wFeatureSelector);
extern uint32_t CDC_GetLineCoding            (void);
extern uint32_t CDC_SetLineCoding            (void);
extern uint32_t CDC_SetControlLineState      (unsigned short wControlSignalBitmap);
extern uint32_t CDC_SendBreak                (unsigned short wDurationOfBreak);

/* CDC Bulk Callback Functions */
extern void CDC0_BulkIn                   (void);
extern void CDC0_BulkOut                  (void);

extern void CDC1_BulkIn                   (void);
extern void CDC1_BulkOut                  (void);

extern void CDC2_BulkIn                   (void);
extern void CDC2_BulkOut                   (void);

extern void CDC3_BulkIn                   (void);
extern void CDC3_BulkOut                  (void);

extern void CDC4_BulkIn                   (void);
extern void CDC4_BulkOut                   (void);

/* CDC Notification Callback Function */
extern void CDC0_NotificationIn           (void);
extern void CDC1_NotificationIn           (void);

/* CDC Initializtion Function */
extern void CDC_Init (char portNum);

/* CDC prepare the SERAIAL_STATE */
extern unsigned short CDC0_GetSerialState (void);
extern unsigned short CDC1_GetSerialState (void);
extern unsigned short CDC2_GetSerialState (void);
extern unsigned short CDC3_GetSerialState (void);

/* flow control */
extern unsigned short CDC0_DepInEmpty;         // DataEndPoint IN empty
extern unsigned short CDC1_DepInEmpty;         // DataEndPoint IN empty
extern unsigned short CDC2_DepInEmpty;         // DataEndPoint IN empty
extern unsigned short CDC3_DepInEmpty;         // DataEndPoint IN empty

#endif  /* __CDCUSER_H__ */

