/**
 * \file rotation.cpp
 */

#include "rotation.h"

Rotation::Rotation() : angleCourant_(0), asservissement_(5,300,0)
{
}

int32_t Rotation::angleCourant()
{
	return angleCourant_;
}

void Rotation::angleCourant(int32_t angleCourant)
{
	angleCourant_ = angleCourant;
}

void Rotation::reset()
{
}
