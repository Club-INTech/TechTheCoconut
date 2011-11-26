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
		
	private:
		Asservissement asservissement_;
		
		/**
		 * Contient la distance courante en mm*10
		 * 
		 * \Warning 32 bits sont-ils suffisants (= 1024) ??
		 */
		uint32_t distanceCourante;		
		
		/**
		 * Getter pour la distance courante
		 * 
		 * \return uint32_t distanceCourante
		 */
		uint32_t recupererDistance();
		
		/**
		 * Remet à zéro l'asservissement en translation en réinitialisant les données
		 * 
		 * \return bool FALSE si reset réussi, TRUE sinon
		 */
		bool reset();
};


#endif
