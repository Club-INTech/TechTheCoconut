/**
 * \file translation.cpp
 */

#include "translation.h"

Translation::Translation() : asservissement_(3,200,0), consigne_(0)
{
}

int16_t Translation::pwm(int32_t distanceCourante)
{
	return asservissement_.pwm(consigne_,distanceCourante);
}

int32_t Translation::consigne()
{
	return consigne_;
}

void Translation::consigne(int32_t consigne)
{
	consigne_ = consigne;
}

int32_t Translation::vitesse()
{
	return vitesse_;
}

void Translation::vitesse(int32_t vitesse)
{
	vitesse_ = vitesse;
}

void Translation::reset()
{
}
