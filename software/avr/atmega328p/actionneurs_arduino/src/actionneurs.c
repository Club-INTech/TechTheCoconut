#include "actionneurs.h"
#include "ax12.h"

#include <libintech/serial/serial_0.hpp>


void AX12InitID(uint8_t ID)
{
    writeData (1, AX_ID, 1, ID);
}

void AX12SetLeds(uint8_t ID, byte masque)
{
    writeData(ID, AX_LED, 1, masque);
    writeData(ID, AX_ALARM_LED, 1, masque);
}

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

void AX12GOTO(uint8_t ID, uint16_t angle)
{
    Serial<0>::print(0xFF);
    Serial<0>::print(0xFF);
        
}

void extraction(unsigned char x, char *x1, char *x2)
{
    char tmp = x >> 5;
    *x1 = tmp & 0b00000011;
    *x2 = x & 0b00011111;
}

void extraction_consigne(unsigned char x, char *cons)
{
    *cons = x >> 7;
}

void AX12Unasserv(uint8_t ID)
{
    writeData (ID, AX_TORQUE_ENABLE, 1, 0);
}

    