/**
 * \file translation.cpp
 */

#include "translation.h"

Translation::Translation() : asservissement_(3,200,0), distanceCourante_(0)
{
}

int32_t Translation::distanceCourante()
{
	return distanceCourante_;
}

void Translation::distanceCourante(int32_t distanceCourante)
{
	distanceCourante_ = distanceCourante;
}

void Translation::reset()
{
}
