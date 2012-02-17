/**
 * \file balise.h
 *
 * Classe représentant la balise
 */

#ifndef Balise_h
#define Balise_h

#include <stdint.h>
#include <libintech/singleton.hpp>
#include "utils.h"

class Balise : public Singleton<Balise>{
	private:
		uint16_t max_counter_;
	public:
		void max_counter(uint16_t valeur);
		float getAngle();
};


#endif
