/**
 * \file frame.h
 *
 * Classe représentant une frame
 */

#ifndef Frame_h
#define Frame_h

#include <stdint.h>
#include "crc8.h"

class Frame {
	
	public:
		Frame(char rawFrame[3]);
		bool isValid();
		unsigned char getRobotId();
		uint16_t getDistance();

	private:
		uint16_t data_;
		unsigned char robotId_;
		uint16_t distance_;
		uint8_t crc_;
};


#endif
