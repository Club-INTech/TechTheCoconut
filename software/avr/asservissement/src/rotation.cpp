/**
 * \file rotation.cpp
 */

#include "rotation.h"

Rotation::Rotation() : angleCourant_(0)
{
	asservissement_.activationKd(1);
	
	// initialisation des constantes
	asservissement_.kp(5);
	asservissement_.pwm(PWM_MAX);
	asservissement_.kd(300);
	asservissement_.ki(0);
	asservissement_.vMax(0);
	asservissement_.kpVitesse(0);

}

int32_t Rotation::recupererAngle()
{
	return angleCourant_;
}

bool Rotation::reset()
{
	return false;
}