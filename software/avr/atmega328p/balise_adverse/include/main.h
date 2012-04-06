#ifndef _MAIN_H_
#define _MAIN_H_

/**
 * Programme de la balise placée sur un robot adverse et qui envoie une trame contenant la distance au passage des lasers sur les photo-diodes.
 * @file main.h
 * @author Paul Bernier avec le support stylistique de Philippe Tillet
 * @brief Programme de la balise sur le robot adverse
 * @version 1.0
 * @date 18/01/2012
 */
#include <libintech/serial/serial_0_interrupt.hpp>
#include <libintech/serial/serial_0.hpp>
#include <avr/io.h>
#include <stdint.h>  
#include <avr/interrupt.h>
#include "utils.h"
#include "frame.h"
#include "timeToDistance.h"
#include "crc8.h"



/**
 * @defgroup binary
 * @brief Macros de manipulations de bits
 * Ces macros permettent de manipuler de façon claire un bit donné d'un port donné.
 */
 
#ifndef sbi
/**
 * @ingroup binary
 * @def sbi(port,bit)
 * @brief Met à 1 le bit du port
 * @param port Port concerné
 * @param bit Bit concerné
 * Met à 1 le bit du port.
 */
#define sbi(port,bit) (port) |= (1 << (bit))
#endif

/**
 * @ingroup binary
 * @def cbi(port,bit)
 * @brief Met à 0 le bit du port
 * @param port Port concerné
 * @param bit Bit concerné
 * Met à 0 le bit du port.
 */
#ifndef cbi
#define cbi(port,bit) (port) &= ~(1 << (bit))
#endif

/**
 * @ingroup binary
 * @def tbi(port,bit)
 * @brief Bascule (toggle) le bit du port
 * @param port Port concerné
 * @param bit Bit concerné
 * Bascule (toggle) le bit du port (0 -> 1 et 1 -> 0)
 */
#ifndef tbi
#define tbi(port,bit) (port) ^= (1 << (bit))
#endif

#ifndef rbi
#define rbi(port,bit) ((port & (1 << bit)) >> bit)
#endif

/**
 * @fn void void setup()
 * @brief Initialise l'environnement
 * Cette fonction initialise les registres, librairies et variables nécessaires aux besoins du programme.
 */
void setup();

#endif

