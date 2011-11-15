#ifndef Rotation_h
#define Rotation_h

#include <stdint.h>

#include "asservissement.h"

class Rotation {
	public:
		Rotation();
		
		int8_t reset();
		
	private:
		Asservissement asservissement_;
};


#endif
