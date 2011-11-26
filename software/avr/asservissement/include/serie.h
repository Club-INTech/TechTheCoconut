/**
 * \file serie.h
 */

#ifndef Serie_h
#define Serie_h

#include <stdint.h>

#include "usart.h"

#include "asservissement.h"

class Serie {
	public:
		Serie();
		
		/**
		 * Traite l'information donnée pour qu'elle soit transmise à l'AVR par port série
		 * 
		 * \return bool FALSE si traitement réussi, TRUE sinon
		 */
		bool traiter();
};


#endif
