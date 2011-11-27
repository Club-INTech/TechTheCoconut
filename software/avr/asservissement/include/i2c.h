/**
 * \file i2c.h
 * 
 * Classe permettant de gérer la liaison I2c
 */

#ifndef I2c_h
#define I2c_h

#include <stdint.h>

#include "rotation.h"
#include "translation.h"

#include "twi_master.h"

class I2c {
	public:
		/**
		 * Constructeur
		 */
		I2c();
		
		/**
		 * Destructeur
		 */
		~I2c();
};


#endif
