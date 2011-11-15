#ifndef Translation_h
#define Translation_h

#include <stdint.h>

#include "asservissement.h"

class Translation {
	public:
		Translation();
		
		int8_t reset();
		
	private:
		Asservissement asservissement_;
};


#endif
