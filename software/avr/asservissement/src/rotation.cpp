/**
 * \file rotation.cpp
 */

#include "rotation.h"

Rotation::Rotation() : asservissement_(5,300,0), consigne_(0)
{
}

int16_t Rotation::pwm(int32_t distanceCourante)
{
	return asservissement_.pwm(consigne_,distanceCourante);
}

int32_t Rotation::consigne()
{
	return consigne_;
}

void Rotation::consigne(int32_t consigne)
{
	consigne_ = consigne;
}

int32_t Rotation::vitesse()
{
	return vitesse_;
}

void Rotation::vitesse(int32_t vitesse)
{
	vitesse_ = vitesse;
}

void Rotation::reset()
{
}
