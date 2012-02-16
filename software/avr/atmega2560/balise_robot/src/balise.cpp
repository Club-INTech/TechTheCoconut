/**
 * \file balise.cpp
 */

#include "balise.h"

float Balise::getAngle() {
	ClasseTimer &angle_counter = ClasseTimer::Instance();
	int speed = 25;//Tour/s
	int max_counter = 65536/speed;
	
	return angle_counter.value()*360/max_counter;
}

