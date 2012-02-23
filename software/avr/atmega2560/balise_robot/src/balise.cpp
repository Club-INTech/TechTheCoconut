/**
 * \file balise.cpp
 */
#include "balise.h"
#include <libintech/serial/serial_0.hpp>

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}
float Balise::getAngle() {
	while(!is_toptour_available_){ asm("nop"); }
	return ((float) toptour_)*360/((float) max_counter_);
}

Balise::Balise()  : is_toptour_available_(true)//: asservissement_moteur_(0.5,0.5,0)
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
	while(!is_toptour_available_){ asm("nop"); }
	is_toptour_available_ = false;
	toptour_++;
	is_toptour_available_ = true;
}

void Balise::reset_toptour()
{
	while(!is_toptour_available_){ asm("nop"); }
	is_toptour_available_ = false;
	toptour_=0;
	is_toptour_available_ = true;
}

uint16_t Balise::toptour()
{
	while(!is_toptour_available_){ asm("nop"); }
	return toptour_;
}
