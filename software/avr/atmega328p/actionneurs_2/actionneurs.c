#include "actionneurs.h"
#include "ax12.h"


void AX12Init (uint8_t ID, uint16_t angleCW, uint16_t angleCCW, uint16_t vitesse)
{
    // Fonction bas niveau pour la transmission série
    ax12Init_ (BAUD_RATE_SERIE);
    // Active l'asservissement du servo
    writeData_ (ID, AX_TORQUE_ENABLE, 1, 1);
    // Définit les angles mini et maxi
    writeData_ (ID, AX_CW_ANGLE_LIMIT_L, 2, angleCW);
    writeData_ (ID, AX_CCW_ANGLE_LIMIT_L, 2, angleCCW);
    // Définit la vitesse de rotation
    writeData_ (ID, AX_GOAL_SPEED_L, 2, vitesse);

}

void AX12GoTo (uint8_t ID, uint16_t angle)
{
    writeData_ (ID, AX_GOAL_POSITION_L, 2, angle);
}
