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
		 * Getter pour l'angle courant
		 * 
		 * \return int32_t angleCourant
		 */
		int32_t recupererAngle();
		
		/**
		 * Remet à zéro l'asservissement en rotation en réinitialisant les données
		 * 
		 * \return bool FALSE si reset réussi, TRUE sinon
		 */
		bool reset();
	private:
		/**
		 * Angle courant en degrés*10
		 * 
		 * \Warning 32 bits sont-ils suffisants (= 1024) ??
		 */
		int32_t angleCourant_;
		
		Asservissement asservissement_;
};


#endif
