/**
 * \file balise.cpp
 */
#include "balise.h"
#include <libintech/serial/serial_0.hpp>

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}
float Balise::getAngle() {
	return ((float) toptour_)*360/((float) max_counter_);
}

Balise::Balise() //: asservissement_moteur_(0.5,0.5,0)
{
	Serial<0>::init();
	
}
/*
void Balise::asservir(int32_t vitesse_courante)
{
	moteur_.envoyerPwm(asservissement_moteur_.pwm(vitesse_courante));
}*/

void Balise::incremente_toptour()
{
	toptour_++;
}

void Balise::reset_toptour()
{
	toptour_=0;
}

uint16_t Balise::toptour()
{
	return toptour_;
}
