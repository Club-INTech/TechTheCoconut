#ifndef _UTILS_H_
#define _UTILS_H_

/**
 * Défini l'intervalle de temps minimum à prendre en considération pour une double impulsion
 * @def TIME_THRESHOLD_MIN
 */
#define TIME_THRESHOLD_MIN 100

/**
 * Défini l'id du "gros" robot adverse
 * @def GROS_ROBOT
 */
#define GROS_ROBOT 0
/**
 * Défini l'id du "petit" robot adverse
 * @def PETIT_ROBOT
 */
#define PETIT_ROBOT 1
/**
 * Défini l'id du robot adverse sur lequelle est placé ce code
 * @def ROBOT
 */
#define ROBOT GROS_ROBOT

#ifndef _FRAME_TYPEDEF_
#define _FRAME_TYPEDEF_
/**
 * Défini le type Frame sur 32 bits
 * @def Frame
 */
typedef uint32_t Frame;
/**
 * Défini le type Data sur 16 bits
 * @def Data
 */
typedef uint16_t Data;
/**
 * Défini le type Crc sur 8 bits
 * @def Crc
 */
typedef uint8_t Crc;
#endif

#endif
