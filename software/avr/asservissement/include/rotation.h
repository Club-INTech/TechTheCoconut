/**
 * \file rotation.h
 */

#ifndef Rotation_h
#define Rotation_h

#include <stdint.h>

#include "asservissement.h"

class Rotation {
	public:
		Rotation();
		
		/**
		 * Remet à zéro l'asservissement en rotation en réinitialisant les données
		 * 
		 * \return bool FALSE si reset réussi, TRUE sinon
		 */
		bool reset();
		
	private:
		Asservissement asservissement_;
};


#endif
