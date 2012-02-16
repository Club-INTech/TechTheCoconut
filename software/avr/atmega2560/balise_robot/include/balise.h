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
	
	public:
		float getAngle();
};


#endif
