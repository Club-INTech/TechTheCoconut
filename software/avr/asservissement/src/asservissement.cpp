/**
 * \file asservissement.cpp
 */

#include "asservissement.h"

//Je laisse ces define pour le moment, mais à refaire type-safe.
#define ABS(x)      ((x) < 0 ? - (x) : (x))
#define MAX(a,b)    ((a) > (b) ? (a) : (b)) 
#define MIN(a,b)    ((a) < (b) ? (a) : (b)) 


Asservissement::Asservissement(int16_t kp, int16_t kd, int16_t ki) : kp_(kp), kd_(kd), ki_(ki)
{
}

int16_t Asservissement::pwm(int32_t consigne, int32_t positionReelle)
{
    int32_t erreur = positionReelle - consigne;
    // Pour l'instant, que kp ; on incrémentera après.  
    return kp_ * erreur/5;
}

/*
 * Arrêt progressif du moteur
 */ 
void Asservissement::stop()
{

}

/*
 * Définition dynamique des constantes
 */
void Asservissement::kp(uint16_t kp)
{
    kp_ = kp;
}

uint16_t Asservissement::kp(void)
{
   return kp_;
}

void Asservissement::ki(uint16_t ki)
{
    ki_ = ki;
}

uint16_t Asservissement::ki(void)
{
    return ki_;
}

void Asservissement::kd(uint16_t kd)
{
    kd_ = kd;
}

uint16_t Asservissement::kd(void)
{
    return kd_;
}
