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
	unsigned char consigneActuelle = '\0';
	//
	 // Constante de l'asservissement et du mouvement
    maxPWM =    0;
    kp =        0;
    vMax =      0;
    kd =        0;
    ki =        0;
    kpVitesse = 0;
    
    // Consigne par défaut et position du robot à l'initialisation
    integraleErreur=0;

    // Vitesse du robot
    vitesse = 0;

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
	
    int32_t pwm = kp * erreur/5 + activationKd * kd * vitesse/100  - ki  * integraleErreur;
	
    if (vitesse > vMax) {
        // pas besoin de dérivateur ou d'intégrateur ici
		
        pwm += kpVitesse * (vMax - vitesse); 
    }

    if (pwm > maxPWM) {
        pwm = maxPWM;
    }
    
    if (pwm < -maxPWM ) {
        pwm = -maxPWM;
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
void Asservissement::changeKp(uint16_t kpDonne)
{
    kp = kpDonne;
}

void Asservissement::changePWM(int16_t maxPwmDonne)
{
    maxPWM = maxPwmDonne;
}

void Asservissement::changeVmax(int32_t vMaxDonne)
{
    vMax = vMaxDonne;
}

void Asservissement::changeKd(uint16_t kdDonne)
{
    kd = kdDonne;
}

void Asservissement::setActivationKd(unsigned char etatDonne)
{
    activationKd = etatDonne;
}

void Asservissement::changeKi(uint16_t kiDonne)
{
    ki = kiDonne;
}

void Asservissement::changeKpVitesse(uint16_t kpVitesseDonne)
{
    kpVitesse=kpVitesseDonne;
}

void Asservissement::setVitesse(int32_t vitesseDonnee)
{
    vitesse = vitesseDonnee;
}