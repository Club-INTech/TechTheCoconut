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

// Librairie locale.
#include "ax12.h"

// ID de broadcast : tous les AX12 éxécutent les ordres
// envoyés à cet ID.
#define AX_BROADCAST            0xFE

// Angles MIN et MAX en tics (compris entre 0 et 1024, cf. datasheet)
#define AX_ANGLECW              198
#define AX_ANGLECCW             800

// Vitesse de rotation des AX12 (je crois entre 0 et 1024, pas sûr)
#define AX_SPEED                1000


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
/// \param ID       Nouvel ID à donner à l'AX12 branché
/// Tous les AX12 branchés changeront leurs ID actuels pour ce nouvel ID.

void AX12InitID(uint8_t ID);


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


#endif
