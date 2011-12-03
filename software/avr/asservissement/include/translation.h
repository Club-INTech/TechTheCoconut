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
		 * \return int32_t distanceCourante_
		 */
		int32_t distanceCourante();

		/**
		 * Setter pour la distance courante
		 */
		void distanceCourante(int32_t);
		
		/**
		 * Remet à zéro l'asservissement en translation en réinitialisant les données
		 * [Ronald: ] Enlevé valeur de retour, voir Rotation.
		 */
		void reset();
		
	private:
		Asservissement asservissement_;
		
		/**
		 * Contient la distance courante en tics
		 * 
		 * \Warning 32 bits sont-ils suffisants (= 1024) ??
		 * [Ronald:] 2^32 = 4 294 967 296 :p
		 */
		int32_t distanceCourante_;		
};


#endif
