#ifndef _TIMETODISTANCE_H_
#define _TIMETODISTANCE_H_

#include <stdint.h>
#include "table.h"

/**
 * @fn uint16_t getDistance(uint16_t delta)
 * @brief Renvoie la distance correspondant à un écart de temps donné
 * @param delta Ecart de temps en µs
 * Retourne une distance en mm à partir d'un écart de temps en µs grâce à la table.
 */
uint16_t getDistance(uint16_t delta);

/**
 * @fn inline uint16_t linearReg(int32_t x, int32_t x1, int32_t y1, int32_t x2, int32_t y2)
 * @brief Régression linéaire entre deux points
 * Retourne l'ordonnée du point d'abscisse x entre les points (x1,y1) et (x2,y2).
 */
inline uint16_t linearReg(int32_t x, int32_t x1, int32_t y1, int32_t x2, int32_t y2);

#endif
