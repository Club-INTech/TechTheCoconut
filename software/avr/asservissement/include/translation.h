/**
 * \file translation.h
 */

#ifndef Translation_h
#define Translation_h

#include <stdint.h>

#include "asservissement.h"

class Translation {
	public:
		Translation();
		
		/**
		 * Getter pour la distance courante
		 * 
		 * \return uint32_t distanceCourante_
		 * 
		 * J'ai mis un nom plus conventionnel
		 */
		uint32_t translationCourante();
		
		/**
		 * Remet à zéro l'asservissement en translation en réinitialisant les données
		 * 
		 * \return bool FALSE si reset réussi, TRUE sinon
		 */
		bool reset();
		
	private:
		Asservissement asservissement_;
		
		/**
		 * Contient la distance courante en mm*10
		 * 
		 * \Warning 32 bits sont-ils suffisants (= 1024) ??
		 * 2^32 = 4 294 967 296 :p
		 */
		uint32_t translationCourante_;		
};


#endif
