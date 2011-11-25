/**
 * \file asservissement.cpp
 */

#include "asservissement.h"

Asservissement::Asservissement()
{
	//Bug si =''
	unsigned char consigneActuelle = '\0';
}

unsigned char Asservissement::recupererConsigne()
{
	return consigneActuelle;
}