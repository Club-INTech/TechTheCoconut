#ifndef ACTIONNEURS_H
#define ACTIONNEURS_H

/** @file avr/atmega324p/actionneurs/include/actionneurs.hpp
 *  @brief Ce fichier crée les constantes haut niveau pour les actionneurs.
 *  @author Thibaut ~MissFrance~
 *  @date 05 mai 2012
 */ 

// Librairies standard
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// ID de broadcast : tous les AX12 éxécutent les ordres
// envoyés à cet ID.
#define AX_BROADCAST            0xFE

// Angles MIN et MAX en tics (compris entre 0 et 1024, cf. datasheet)
#define AX_ANGLECW              198
#define AX_ANGLECCW             800

// Vitesse de rotation des AX12 (je crois entre 0 et 1024, pas sûr)
#define AX_SPEED                1000


/** EEPROM AREA **/
#define AX_MODEL_NUMBER_L           0
#define AX_MODEL_NUMBER_H           1
#define AX_VERSION                  2
#define AX_ID                       3
#define AX_BAUD_RATE                4
#define AX_RETURN_DELAY_TIME        5
#define AX_CW_ANGLE_LIMIT_L         6
#define AX_CW_ANGLE_LIMIT_H         7
#define AX_CCW_ANGLE_LIMIT_L        8
#define AX_CCW_ANGLE_LIMIT_H        9
#define AX_SYSTEM_DATA2             10
#define AX_LIMIT_TEMPERATURE        11
#define AX_DOWN_LIMIT_VOLTAGE       12
#define AX_UP_LIMIT_VOLTAGE         13
#define AX_MAX_TORQUE_L             14
#define AX_MAX_TORQUE_H             15
#define AX_RETURN_LEVEL             16
#define AX_ALARM_LED                17
#define AX_ALARM_SHUTDOWN           18
#define AX_OPERATING_MODE           19
#define AX_DOWN_CALIBRATION_L       20
#define AX_DOWN_CALIBRATION_H       21
#define AX_UP_CALIBRATION_L         22
#define AX_UP_CALIBRATION_H         23

/** RAM AREA **/
#define AX_TORQUE_ENABLE            24
#define AX_LED                      25
#define AX_CW_COMPLIANCE_MARGIN     26
#define AX_CCW_COMPLIANCE_MARGIN    27
#define AX_CW_COMPLIANCE_SLOPE      28
#define AX_CCW_COMPLIANCE_SLOPE     29
#define AX_GOAL_POSITION_L          30
#define AX_GOAL_POSITION_H          31
#define AX_GOAL_SPEED_L             32
#define AX_GOAL_SPEED_H             33
#define AX_TORQUE_LIMIT_L           34
#define AX_TORQUE_LIMIT_H           35
#define AX_PRESENT_POSITION_L       36
#define AX_PRESENT_POSITION_H       37
#define AX_PRESENT_SPEED_L          38
#define AX_PRESENT_SPEED_H          39
#define AX_PRESENT_LOAD_L           40
#define AX_PRESENT_LOAD_H           41
#define AX_PRESENT_VOLTAGE          42
#define AX_PRESENT_TEMPERATURE      43
#define AX_REGISTERED_INSTRUCTION   44
#define AX_PAUSE_TIME               45
#define AX_MOVING                   46
#define AX_LOCK                     47
#define AX_PUNCH_L                  48
#define AX_PUNCH_H                  49

/** Status Return Levels **/
#define AX_RETURN_NONE              0
#define AX_RETURN_READ              1
#define AX_RETURN_ALL               2

/** Instruction Set **/
#define AX_PING                     1
#define AX_READ_DATA                2
#define AX_WRITE_DATA               3
#define AX_REG_WRITE                4
#define AX_ACTION                   5
#define AX_RESET                    6
#define AX_SYNC_WRITE               131



/// \brief Cette fonction asservit en angle un AX12
/// \param ID       ID de l'AX12 à asservir.
/// \param angle    Nouvel angle (entre 0 et 1024)

void AX12GoTo (uint8_t ID, uint16_t angle);


/// \brief Cette fonction s'occupe d'initialiser les AX12
/// \param ID       ID de l'AX12 à initialiser
/// \param angleCW  Angle MIN
/// \param angleCCW Angle MAX
/// \param vitesse  Vitesse de rotation initiale
/// Cette fonction s'occupe d'initialiser les AX12 (Angle min et max, vitesse), les
/// autorise à tourner et leur donne un couple max.

void AX12Init (uint8_t ID, uint16_t angleCW, uint16_t angleCCW, uint16_t vitesse);


/// \brief Cette fonction réinitialise l'ID d'un AX12 branché.
/// \param ancien_id       Ancien ID de l'AX12.
/// \param nouvel_id       Nouvel ID à donner à l'AX12 branché
/// \warning Tous les AX12 branchés changeront leurs ID actuels pour ce nouvel ID.
void AX12InitID(uint8_t ancien_id, uint8_t nouvel_id);


/// \brief Cette fonction desasservit un AX12
/// \param ID       ID de l'AX12 à desasservir.

void AX12Unasserv(uint8_t ID);


/// \brief Réinitialise l'angle min de l'AX12
/// \param ID       ID de l'AX12
/// \param angleCW  Nouvel angle min (entre 0 et 1024)

void AX12ChangeAngleMIN(uint8_t ID, uint16_t angleCW);


/// \brief Réinitialise l'angle max de l'AX12
/// \param ID       ID de l'AX12
/// \param angleCCW Nouvel angle max (entre 0 et 1024)

void AX12ChangeAngleMAX(uint8_t ID, uint16_t angleCCW);


/// \brief Réinitialise la vitesse de rotation de l'AX12
/// \param ID       ID de l'AX12
/// \param vitesse  Nouvelle vitesse de rotation

void AX12ChangeSpeed(uint8_t ID, uint16_t vitesse);


void reset (uint8_t id);
void writeData (uint8_t id, uint8_t regstart, uint8_t reglength, uint16_t value);


#endif
