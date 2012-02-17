/**
 * \file balise.cpp
 */

#include "balise.h"
#include <libintech/serial/serial_0.hpp>

void Balise::max_counter(uint16_t valeur){
	max_counter_ = valeur;
}
float Balise::getAngle() {
// 	float speed = 12.0/30.0;//Tour/s
	Serial<0>::init();
	Serial<0>::print(max_counter_);
	return ClasseTimer::value()*360/max_counter_;
}