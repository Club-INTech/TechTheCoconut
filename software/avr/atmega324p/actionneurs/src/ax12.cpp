/*
  ax12.c - arbotiX Library for AX-12 Servos
  Copyright (c) 2008,2009 Michael E. Ferguson.  All right reserved.
*/

/** @file avr/atmega324p/actionneurs/include/ax12.cpp
 *  @brief Ce fichier crée les constantes haut niveau pour les actionneurs.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

// Librairie Standard
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

// Librairie INTech.
#include <libintech/serial/serial_1.hpp>

// Librairie locale.
#include "ax12.h"
#include "actionneurs.h"

// Liaison série Carte <-> AX12
typedef Serial<1> serial_ax_;



/******************************************************************************
 * Hardware Serial Level, this uses the same stuff as Serial, therefore 
 *  you should not use the Arduino Serial library.
 ******************************************************************************/


/** Sends a character out the serial port */
uint8_t ax12writeB(uint8_t data){
    serial_ax_::send_char(data);
    return data;
}


/******************************************************************************
 * Packet Level
 ******************************************************************************/

/// Envoi d'un packet vers les AX12, voir datasheet pour comprendre
/// les normes utilisées.
void ax12SendPacket (uint8_t id, uint8_t datalength, uint8_t instruction, uint8_t *data){
    uint8_t checksum = 0;
    ax12writeB(0xFF);
    ax12writeB(0xFF);
    checksum += ax12writeB(id);
    checksum += ax12writeB(datalength + 2);
    checksum += ax12writeB(instruction);

    uint8_t f;
    for (f=0; f<datalength; f++) {
      checksum += ax12writeB(data[f]);
    }
    ax12writeB(~checksum);
}

/******************************************************************************
 * Instruction Level
 ******************************************************************************/

/** ping */
void ping (uint8_t id) {
     uint8_t *data = 0;
     ax12SendPacket (id, 0, AX_PING, data);  
}

/** reset */
void reset (uint8_t id) {
     uint8_t *data = 0;
     ax12SendPacket (id, 0, AX_RESET, data);  
}

/** action */
void action (uint8_t id) {
     uint8_t *data = 0;
     ax12SendPacket (id, 0, AX_ACTION, data); 
}


/** write data */
void writeData (uint8_t id, uint8_t regstart, uint8_t reglength, uint16_t value) {
    uint8_t data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_WRITE_DATA, data);
}

/** reg write */
void regWrite (uint8_t id, uint8_t regstart, uint8_t reglength, uint16_t value) {
    uint8_t data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_REG_WRITE, data);
}

