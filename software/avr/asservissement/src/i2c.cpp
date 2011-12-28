/**
 * \file i2c.cpp
 */

#include "i2c.h"

I2c::I2c()
{
	TWI_init();
	
	// Met à zéro la liaison
	send_reset();
}