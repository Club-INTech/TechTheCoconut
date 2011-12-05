/**
 * \file translation.h
 */

#ifndef Translation_h
#define Translation_h

#include <stdint.h>

#include "asservissement.h"
#include "moteur.h"

 class Translation {
	public:
	
		Translation();
		
		int16_t pwm(int32_t distanceCourante);
		
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
		 * Getter pour la vitesse
		 * 
		 * \return int32_t consigne
		 */
		int32_t vitesse();

		/**
		 * Setter pour la vitesse
		 * 
		 */
		void vitesse(int32_t);	
				
		/**
		 * Remet à zéro l'asservissement en translation en réinitialisant les données
		 * [Ronald: ] Enlevé valeur de retour, voir Rotation.
		 */
		void reset();
		
	private:
		Asservissement asservissement_;
		int32_t consigne_;
		int32_t vitesse_;
};


#endif
