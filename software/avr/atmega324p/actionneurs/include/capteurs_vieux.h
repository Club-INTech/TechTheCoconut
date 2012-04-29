#ifndef CAPTEURS_H
#define CAPTEURS_H

#include <avr/io.h>
#include <stdint.h>

/*
 *  Temps maximal d'attente de la fin d'une impulsion
 *    S'exprimme en nombre de passage dans une boucle, donc depend de cette boucle
 */
#define TIMEOUT 1500

/*
 *  Fonction pour obtenir la distance a partir d'un capteur a ultrasons
 *    Prend la pin du capteur en argument
 */
uint16_t ping_capt(uint8_t pin);

#endif
