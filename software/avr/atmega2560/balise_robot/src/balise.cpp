/**
 * \file balise.cpp
 */

#include "balise.h"
#include <libintech/serial/serial_0.hpp>

Balise::Balise() : asservissement_moteur_(0.5,0.5,0)
{
	Serial<0>::init();
	
}

void Balise::asservir(int32_t vitesse_courante)
{
	moteur_.envoyerPwm(asservissement_moteur_.pwm(vitesse_courante));
}

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}
float Balise::getAngle() {
// 	float speed = 12.0/30.0;//Tour/s
	Serial<0>::init();
	Serial<0>::print(max_counter_);
	return ClasseTimer::value()*360/max_counter_;
}

ISR(TIMER0_OVF_vect){
	Balise & balise = Balise::Instance();
	balise.asservir(balise.vitesse_moteur());
	//printlnLong(robot.x());
}