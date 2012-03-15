/**
 * \file balise.cpp
 */
#include "balise.h"
#include <libintech/serial/serial_0.hpp>

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}

uint16_t Balise::getAngle() {
	return toptour_*360/max_counter_;
}

Balise::Balise() : asservissement_moteur_(0.5,0.5,0)
{
	asservissement_moteur_.consigne(0);
	Serial<0>::init();
	T_Asservissement::init();
	
}

void Balise::asservir(int32_t vitesse_courante)
{
	int16_t pwm = asservissement_moteur_.pwm(vitesse_courante);
// 	Serial<0>::print(pwm);
	moteur_.envoyerPwm(pwm);
}

void Balise::incremente_toptour()
{
	toptour_++;
}

void Balise::reset_toptour()
{
	toptour_=1;
}

uint16_t Balise::toptour()
{
	return toptour_;
}
