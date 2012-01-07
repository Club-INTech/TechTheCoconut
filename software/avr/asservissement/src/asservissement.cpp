/**
* \file asservissement.cpp
*/

#include "asservissement.h"

//Je laisse ces define pour le moment, mais à refaire type-safe.
#define ABS(x)      ((x) < 0 ? - (x) : (x))
#define MAX(a,b)    ((a) > (b) ? (a) : (b))
#define MIN(a,b)    ((a) < (b) ? (a) : (b))


Asservissement::Asservissement(uint16_t kp, uint16_t kd, uint16_t ki) : kp_(kp), kd_(kd), ki_(ki), en_(0), enm1_(0), enm2_(0), pwmCourant_(0),consigne_(0), pwmMax_(255)
{
}

int16_t Asservissement::pwm(int32_t positionReelle)
{	
	enm2_ = enm1_;
	enm1_ = en_;
	en_=consigne_ - positionReelle;
	pwmCourant_+=kp_*(en_ - enm1_) + ki_*en_ + kd_*(en_ - 2*enm1_ + enm2_);
	if(pwmCourant_ > pwmMax_){
		pwmCourant_ = pwmMax_;
	}
	else if(pwmCourant_ < -pwmMax_){
		pwmCourant_ = -pwmMax_;
	}
	return pwmCourant_;
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

void Asservissement::pwmMax(uint16_t pwmMax)
{
	pwmMax_ = pwmMax;
}

uint16_t Asservissement::pwmMax(void)
{
	return pwmMax_;
}

int32_t Asservissement::consigne()
{
	return consigne_;
}

void Asservissement::consigne(int32_t consigne)
{
	consigne_ = consigne;
}

int32_t Asservissement::vitesse()
{
	return vitesse_;
}

void Asservissement::vitesse(int32_t vitesse)
{
	vitesse_ = vitesse;
}

void Asservissement::reset()
{
}


void Asservissement::resetConsignes()
{
}
