/**
 * \file rotation.h
 */

#ifndef Rotation_h
#define Rotation_h

#include <stdint.h>

#include "asservissement.h"
#include "moteur.h"

class Rotation {
	public:
		Rotation();

		/**
		 * Asservir la rotation du robot
		 **/
		 
		int16_t pwm(int32_t angleCourant);
		 
		/**
		 * Getter pour la consigne courante
		 * 
		 * \return int32_t consigne
		 */
		int32_t consigne();

		/**
		 * Setter pour la consigne courante
		 * 
		 */
		void consigne(int32_t);	
		
		/**
		 * Remet à zéro l'asservissement en rotation en réinitialisant les données
		 * Enlevé la valeur de retour car ca ne devrait jamais rater. Et si jamais ça rate, on aura aucun moyen de faire remonter ça dans le code.
		 */
		void reset();
		
	private:
		Asservissement asservissement_;
		int32_t consigne_;
};


#endif
