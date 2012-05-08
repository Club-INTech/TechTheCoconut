/*
  ax12.c - arbotiX Library for AX-12 Servos
  Copyright (c) 2008,2009 Michael E. Ferguson.  All right reserved.
*/

/** @file avr/atmega324p/actionneurs/include/ax12.cpp
 *  @brief Ce fichier crée les constantes haut niveau pour les actionneurs.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

// Librairie INTech
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

// Librairie locale.
#include "ax12.h"
#include "actionneurs.h"


/******************************************************************************
 * Hardware Serial Level, this uses the same stuff as Serial, therefore 
 *  you should not use the Arduino Serial library.
 ******************************************************************************/

byte ax_rx_buffer[AX12_BUFFER_SIZE];
int status_id;
int status_error;
int status_data;

// making these volatile keeps the compiler from optimizing loops of available()
volatile byte ax_rx_Pointer;                       

/// Initialisation de la liaison série AX12 <-> carte.
void AX12_Serial_Init(long baud){
    UBRR0H = (long)((F_CPU / 16 + baud / 2) / baud - 1) >> 8;
    UBRR0L = ((F_CPU / 16 + baud / 2) / baud - 1);
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);
    ax_rx_Pointer = 0;
}

/** Sends a character out the serial port */
byte ax12writeB(byte data){
    while (!( UCSR0A & (1<<UDRE0)));
    UDR0 = data;
    return data; 
}


/******************************************************************************
 * Packet Level
 ******************************************************************************/

/// Envoi d'un packet vers les AX12, voir datasheet pour comprendre
/// les normes utilisées.
void ax12SendPacket (byte id, byte datalength, byte instruction, byte *data){
    byte checksum = 0;
    ax12writeB(0xFF);
    ax12writeB(0xFF);
    checksum += ax12writeB(id);
    checksum += ax12writeB(datalength + 2);
    checksum += ax12writeB(instruction);

    byte f;
    for (f=0; f<datalength; f++) {
      checksum += ax12writeB(data[f]);
    }
    ax12writeB(~checksum);
}

/******************************************************************************
 * Instruction Level
 ******************************************************************************/

/** ping */
void ping (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_PING, data);  
}

/** reset */
void reset (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_RESET, data);  
}

/** action */
void action (byte id) {
     byte *data = 0;
     ax12SendPacket (id, 0, AX_ACTION, data); 
}


/** write data */
void writeData (byte id, byte regstart, byte reglength, int value) {
    byte data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_WRITE_DATA, data);
}

/** reg write */
void regWrite (byte id, byte regstart, byte reglength, int value) {
    byte data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_REG_WRITE, data);
}

