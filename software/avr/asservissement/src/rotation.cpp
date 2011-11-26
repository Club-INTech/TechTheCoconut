/**
 * \file rotation.cpp
 */

#include "rotation.h"
#include "asservissement.h"

Rotation::Rotation()
{
	Asservissement asservissement_;

	int32_t angleCourant = 0;
}

int32_t Rotation::recupererAngle()
{
	return angleCourant;
}

bool Rotation::reset()
{
	return false;
}