#include "compteur.h"
#include "twi_slave.h"
#include "serial.h"

volatile int32_t roue1;
volatile int32_t roue2;

volatile uint8_t etat_codeurs;

unsigned long lol = 0;

void compteur_init (void)
{
    // Initialisation interruptions codeurs
    // Masques
    PCMSK2 |= (1 << PCINT19) | (1 << PCINT18);
    PCMSK1 |= (1 << PCINT9) | (1 << PCINT8);
    // Activer les interruptions
    PCICR |= (1 << PCIE2);
    PCICR |= (1 << PCIE1);

    // Initialisation de l'etat des codeurs
    etat_codeurs = (PIND & CODEUR11) | (PIND & CODEUR12) | (PINC & CODEUR21) | (PINC & CODEUR22);
}

/*
 * Gestion des interruptions sur les pins des codeurs
 * On regarde l'evolution des etats et on deduit le sens de rotation
 * Un schema des signaux aide beaucoup pour comprendre le code
 */


// Interruption codeur 1
ISR (PCINT2_vect)
{
        switch ( etat_codeurs & (CODEUR11 | CODEUR12) ) {
        
        case CODEUR11 | CODEUR12 :
            switch ( PIND & (CODEUR11 | CODEUR12) ) {
                case CODEUR12 :
                    roue1--;
                    break;
                case CODEUR11 :
                    roue1++;
                    break;
                default :
                    break;
            }
            break;
            
        case CODEUR11 :
            switch ( PIND & (CODEUR11 | CODEUR12) ) {
                case CODEUR11 | CODEUR12 :
                    roue1--;
                    break;
                case 0 :
                    roue1++;
                    break;
                default :
                    break;
            }
            break;
            
        case CODEUR12 :
            switch ( PIND & (CODEUR11 | CODEUR12) ) {
                case CODEUR11 | CODEUR12 :
                    roue1++;
                    break;
                case 0 :
                    roue1--;
                    break;
                default :
                    break;
            }
            break;
            
        case 0 :
            switch ( PIND & (CODEUR11 | CODEUR12) ) {
                case CODEUR11 :
                    roue1--;
                    break;
                case CODEUR12 :
                    roue1++;
                    break;
                default :
                    break;
            }
            break;
            
        default :
            break;
    }
    
    etat_codeurs = (PIND & CODEUR11) | (PIND & CODEUR12) | (PINC & CODEUR21) | (PINC & CODEUR22);
    
    //printlnLong(roue1);
}

// Interruption codeur 2
ISR (PCINT1_vect)
{
    switch ( etat_codeurs & (CODEUR21 | CODEUR22) ) {
        
        case CODEUR21 | CODEUR22 :
            switch ( PINC & (CODEUR21 | CODEUR22) ) {
                case CODEUR22 :
                    roue2++;
                    break;
                case CODEUR21 :
                    roue2--;
                    break;
                default :
                    break;
            }
            break;
            
        case CODEUR21 :
            switch ( PINC & (CODEUR21 | CODEUR22) ) {
                case CODEUR21 | CODEUR22 :
                    roue2++;
                    break;
                case 0 :
                    roue2--;
                    break;
                default :
                    break;
            }
            break;
            
        case CODEUR22 :
            switch ( PINC & (CODEUR21 | CODEUR22) ) {
                case CODEUR21 | CODEUR22 :
                    roue2--;
                    break;
                case 0 :
                    roue2++;
                    break;
                default :
                    break;
            }
            break;
            
        case 0 :
            switch ( PINC & (CODEUR21 | CODEUR22) ) {
                case CODEUR21 :
                    roue2++;
                    break;
                case CODEUR22 :
                    roue2--;
                    break;
                default :
                    break;
            }
            break;
            
        default :
            break;
    }
    
    //printlnLong(roue2);
    etat_codeurs = (PIND & CODEUR11) | (PIND & CODEUR12) | (PINC & CODEUR21) | (PINC & CODEUR22);
}

void charger_distance (void)
{
    int32_t distance = roue1 + roue2;

    messageBuf[0] = (uint8_t) distance;
    messageBuf[1] = (uint8_t) (distance >> 8);
    messageBuf[2] = (uint8_t) (distance >> 16);
    messageBuf[3] = (uint8_t) (distance >> 24);
}

void charger_angle (void)
{
    int32_t angle = roue1 - roue2;

    messageBuf[0] = (uint8_t) angle;
    messageBuf[1] = (uint8_t) (angle >> 8);
    messageBuf[2] = (uint8_t) (angle >> 16);
    messageBuf[3] = (uint8_t) (angle >> 24);
}

