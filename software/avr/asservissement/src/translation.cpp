/**
 * \file translation.cpp
 */

#include "translation.h"
#include <stdio.h>

Translation::Translation()
{
	asservissement_.activationKd(1);
	
	// initialisation des constantes
	asservissement_.kp(3);
	asservissement_.pwm(PWM_MAX);
	asservissement_.kd(200);
	asservissement_.ki(0);
	asservissement_.vMax(0);
	asservissement_.kpVitesse(0);

	
	uint32_t distanceCourante = 0;
}

uint32_t Translation::recupererDistance()
{
	return distanceCourante;
}

bool Translation::reset()
{
	return false;
}
