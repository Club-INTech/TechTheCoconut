

/** @file avr/atmega324p/actionneurs/include/actionneurs.cpp
 *  @brief Ce fichier crée les constantes haut niveau pour les actionneurs.
 *  @author Thibaut ~MissFrance~
 *  @date 09 mai 2012
 */ 

// Librairie INTech
#include <libintech/serial/serial_0.hpp>

// Librairie Standard
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>

// Librairie INTech.
#include <libintech/serial/serial_1.hpp>

// Librairie locale.
#include "actionneurs.h"

/// Réinitialisation de l'ID de l'AX12
void AX12InitID(uint8_t ancien_id, uint8_t nouvel_id)
{
    writeData (ancien_id, AX_ID, 1, nouvel_id);
}

/// Initialisation de l'AX12
void AX12Init (uint8_t ID, uint16_t angleCW, uint16_t angleCCW, uint16_t vitesse)
{
    // Active l'asservissement du servo
    writeData (ID, AX_TORQUE_ENABLE, 1, 1);
    // Définit les angles mini et maxi
    writeData (ID, AX_CW_ANGLE_LIMIT_L, 2, angleCW);
    writeData (ID, AX_CCW_ANGLE_LIMIT_L, 2, angleCCW);
    // Définit la vitesse de rotation
    writeData (ID, AX_GOAL_SPEED_L, 2, vitesse);

}

void AX12GoTo (uint8_t ID, uint16_t angle)
{
    writeData (ID, AX_GOAL_POSITION_L, 2, angle);
}

void AX12ChangeAngleMIN(uint8_t ID, uint16_t angleCW)
{
    writeData (ID, AX_CW_ANGLE_LIMIT_L, 2, angleCW);
}

void AX12ChangeAngleMAX(uint8_t ID, uint16_t angleCCW)
{
    writeData (ID, AX_CCW_ANGLE_LIMIT_L, 2, angleCCW);
}

void AX12ChangeSpeed(uint8_t ID, uint16_t vitesse)
{
    writeData (ID, AX_GOAL_SPEED_L, 2, vitesse);
}

void AX12Unasserv(uint8_t ID)
{
    writeData (ID, AX_TORQUE_ENABLE, 1, 0);
}



// Liaison série Carte <-> AX12
typedef Serial<1> serial_ax_;

/******************************************************************************
 * Packet Level  ***  FONCTIONS TRÈS BAS NIVEAU
 ******************************************************************************/

/// Envoi d'un packet vers les AX12, voir datasheet pour comprendre
/// les normes utilisées.
void ax12SendPacket (uint8_t id, uint8_t datalength, uint8_t instruction, uint8_t *data){
    uint8_t checksum = 0;
    serial_ax_::send_char(0xFF);
    serial_ax_::send_char(0xFF);
    
    serial_ax_::send_char(id);
    serial_ax_::send_char(datalength + 2);
    serial_ax_::send_char(instruction);
    
    checksum += id + datalength + 2 + instruction;

    uint8_t f;
    for (f=0; f<datalength; f++) {
      checksum += data[f];
      serial_ax_::send_char(data[f]);
    }
    serial_ax_::send_char(~checksum);
}

/******************************************************************************
 * Instruction Level
 ******************************************************************************/

/** reset */
void reset (uint8_t id) {
     uint8_t *data = 0;
     ax12SendPacket (id, 0, AX_RESET, data);  
}


/** write data */
void writeData (uint8_t id, uint8_t regstart, uint8_t reglength, uint16_t value) {
    uint8_t data [reglength+1];
    data [0] = regstart; data [1] = value&0xFF;
    if (reglength > 1) {data[2] = (value&0xFF00)>>8;}
    ax12SendPacket (id, reglength+1, AX_WRITE_DATA, data);
}

    