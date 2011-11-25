/**
 * \file translation.cpp
 */

#include "translation.h"
#include "asservissement.h"
#include <stdio.h>

Translation::Translation()
{
	Asservissement asservissement_;
	
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
