#ifndef _FRAME_H_
#define _FRAME_H_

#include <stdint.h>
#include "utils.h"
#include "crc8.h"
#include <libintech/serial/serial_0.hpp>


/**
 * @fn Frame makeFrame(uint16_t distance)
 * @brief Permet de forger une trame
 * @param distance Distance à forger dans la trame
 * Forge une trame, c'est à dire ajoute le bit d'identification du robot, le code crc8 et le caractère de terminaison.
 */
Frame makeFrame(uint16_t distance);

/**
 * @fn void sendFrame(Frame frame)
 * @brief Envoie une trame sur la liaison série
 * @param frame Frame à envoyer
 * Envoie une trame sur la série en la découpant en 4 octets.
 */
void sendFrame(Frame frame);

#endif
