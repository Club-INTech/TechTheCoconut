#ifndef robot_h
#define robot_h

#include <stdint.h>
#include "usart.h"

#include "i2c.h"
#include "rotation.h"
#include "translation.h"

/**
 * Structure principale Robot
 */
struct Robot {
	Translation translation; 
	Rotation rotation;
	I2c i2c;
};

#endif