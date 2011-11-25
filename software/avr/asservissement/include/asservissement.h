/**
 * \file asservissement.h
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>

class Asservissement {
	public:
		Asservissement();
	private:
		/**
		 * Consigne actuelle donnée à par l'asservissement à la liaison série
		 */
		unsigned char consigneActuelle;
		
		/**
		 * Getter pour la consigne actuelle
		 * 
		 * \return unsigned char consigneActuelle
		 */
		unsigned char recupererConsigne();
};


#endif
