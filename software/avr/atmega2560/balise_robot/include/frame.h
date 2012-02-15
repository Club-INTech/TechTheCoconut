/**
 * \file frame.h
 *
 * Classe représentant une frame
 */

#ifndef Frame_h
#define Frame_h

#include <stdint.h>

class Frame {
	
	public:
		Frame(uint32_t frame);
		bool isValid();
		unsigned char getRobotId();
		uint16_t getDistance();

	private:
		uint16_t data;
		unsigned char robotId;
		uint16_t distance;
		uint8_t crc;
};


#endif
