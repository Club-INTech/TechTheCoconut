#ifndef CAPTEURS_H
#define CAPTEURS_H

#include <avr/io.h>
#include <stdint.h>

/*
 *  Pins des ultrasons relies a la carte
 */
#define PIN_ULTRASON1   (1 << PORTD6)
#define PIN_ULTRASON2   (1 << PORTD2)

/*
 *  Temps maximal d'attente de la fin d'une impulsion
 *    S'exprimme en nombre de passage dans une boucle, donc depend de cette boucle
 */
#define TIMEOUT 1500

/*
 *  Fonction pour obtenir la distance a partir d'un capteur a ultrasons
 *    Prend la pin du capteur en argument
 */
uint16_t ping(uint8_t pin);

/*
 *  Valeurs enregistrees par les ultrasons
 */
extern volatile uint16_t ultrason;

/*
 *  Pins des capteurs tout ou rien
 */
#define PIN_BRAS1   (1 << PORTB2)
#define PIN_BRAS2   (1 << PORTB1)
#define PIN_JUMPER  (1 << PORTD7)
#define PIN_CENTRE  (1 << PORTC1)

#endif
