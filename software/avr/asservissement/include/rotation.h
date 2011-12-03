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
		int32_t angleCourant();
	
		 /**
		 * Setter pour l'angle courant
		 */
		void angleCourant(int32_t);
		
		/**
		 * Remet à zéro l'asservissement en rotation en réinitialisant les données
		 * Enlevé la valeur de retour :
		 * 	Ca ne devrait jamais rater. Et si jamais ça rate, on aura aucun moyen de faire remonter ça dans le code.
		 */
		void reset();
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
