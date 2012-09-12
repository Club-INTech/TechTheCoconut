#include "actionneurs.h"
#include "ax12.h"

/** @file avr/atmega324p/actionneurs/include/actionneurs.cpp
 *  @brief Ce fichier crée les constantes haut niveau pour les actionneurs.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 
// Librairie INTech
#include <libintech/serial/serial_0.hpp>

/// Initialisation de l'ID de tous les AX12 branchés.
void AX12InitID(uint8_t ID)
{
    writeData (0xFE, AX_ID, 1, ID);
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

    