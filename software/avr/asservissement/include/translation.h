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
		 * Remet à zéro l'asservissement en translation en réinitialisant les données
		 * 
		 * \return bool FALSE si reset réussi, TRUE sinon
		 */
		bool reset();
		
	private:
		Asservissement asservissement_;
};


#endif
