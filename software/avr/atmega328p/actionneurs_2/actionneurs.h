#ifndef ACTIONNEURS_H
#define ACTIONNEURS_H

#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>

/*
 *  Constantes
 *    PWM max pour les maxons
 *    facteur proportionnel
 *    ID des AX12
 *    PWM pour les servos
 *    Type d'asservissement
 */
#define AX_ID1                 1
#define AX_ID2                 2
#define AX_BROADCAST           0xFE

#define AX_ANGLECW              211
#define AX_ANGLECCW             811
#define AX_SPEED               511

#define BAUD_RATE_SERIE        57600

/*
 *  Fonctions pour les AX12
 *    ID : ID du servo
 *    angleCW : angle max antitrigo
 *    angleCCW : angle max trigo
 *    angle : consigne en angle
 *    vitesse : vitesse de rotation
 */
void AX12Init (uint8_t ID, uint16_t angleCW, uint16_t angleCCW, uint16_t vitesse);
void AX12GoTo (uint8_t ID, uint16_t angle);


#endif
