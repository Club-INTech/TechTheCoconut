#ifndef robot_h
#define robot_h

#include <stdint.h>
#include "usart.h"

#include "i2c.h"
#include "rotation.h"
#include "translation.h"
#include "moteur.h"
#include "timer.h"

/**
 * Structure principale Robot
 */
class Robot {
public:
	Robot();
	void asservir();
private:
	Translation translation_; 
	Rotation rotation_;
	Moteur moteurGauche_;
	Moteur moteurDroit_;
	Timer compteur_;
};

#endif
