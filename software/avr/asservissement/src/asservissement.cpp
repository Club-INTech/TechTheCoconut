/**
 * \file asservissement.cpp
 */

#include "asservissement.h"

#define ABS(x)      ((x) < 0 ? - (x) : (x))
#define MAX(a,b)    ((a) > (b) ? (a) : (b)) 
#define MIN(a,b)    ((a) < (b) ? (a) : (b)) 


Asservissement::Asservissement()
{
	//Bug si =''
	// unsigned char consigneActuelle = '\0';
	
	// Constante de l'asservissement et du mouvement
    maxPWM_ =    0;
    kp_ =        0;
    vMax_ =      0;
    kd_ =        0;
    ki_ =        0;
    kpVitesse_ = 0;
    
    // Consigne par défaut et position du robot à l'initialisation
    integraleErreur=0;

    // Vitesse du robot
    vitesse_ = 0;

    // Aucun blocage à l'initialisation
    blocageDetecte = 0;
    blocageTemp = 0;
    
    erreur = 0;
    erreurBkp = 0;
}

unsigned char Asservissement::recupererConsigne()
{
	return consigneActuelle;
}


int32_t Asservissement::calculePwm(int32_t consigne, int32_t positionReelle)
{
    int32_t erreur = positionReelle - consigne;
   
    if (erreur <= 3)
        integraleErreur=0;
    else
        integraleErreur+=erreur;
    
    // la dérivée de l'erreur est égale à -vitesse . On divise par 100 car sinon kd < 1
	
    int32_t pwm = kp_ * erreur/5 + activationKd_ * kd_ * vitesse_/100  - ki_  * integraleErreur;
	
    if (vitesse_ > vMax_) {
        // pas besoin de dérivateur ou d'intégrateur ici
		
        pwm += kpVitesse_ * (vMax_ - vitesse_); 
    }

    if (pwm > maxPWM_) {
        pwm = maxPWM_;
    }
    
    if (pwm < -maxPWM_ ) {
        pwm = -maxPWM_;
    }
    
    return pwm;
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
void Asservissement::kp(uint16_t kpDonne)
{
    kp_ = kpDonne;
}

uint16_t Asservissement::kp(void)
{
   return kp_;
}

void Asservissement::activationKd(unsigned char etatDonne)
{
    activationKd_ = etatDonne;
}

void Asservissement::kpVitesse(uint16_t kpVitesseDonne)
{
    kpVitesse_=kpVitesseDonne;
}

uint16_t Asservissement::kpVitesse(void)
{
    return kpVitesse_;
}

void Asservissement::ki(uint16_t kiDonne)
{
    ki_ = kiDonne;
}

uint16_t Asservissement::ki(void)
{
    return ki_;
}

void Asservissement::kd(uint16_t kdDonne)
{
    kd_ = kdDonne;
}

uint16_t Asservissement::kd(void)
{
    return kd_;
}

void Asservissement::pwm(int16_t maxPwmDonne)
{
    maxPWM_ = maxPwmDonne;
}

int16_t Asservissement::pwm(void)
{
    return maxPWM_;
}

void Asservissement::vMax(int32_t vMaxDonne)
{
    vMax_ = vMaxDonne;
}

int32_t Asservissement::vMax(void)
{
    return vMax_;
}

void Asservissement::vitesse(int32_t vitesseDonnee)
{
    vitesse_ = vitesseDonnee;
}

int32_t Asservissement::vitesse(void)
{
    return vitesse_;
}