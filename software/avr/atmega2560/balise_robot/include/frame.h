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
		Frame(uint32_t rawFrame);
		bool isValid();
		uint16_t getDistance();
		uint16_t getOffset();
		uint8_t getCrc();

	private:
		volatile uint32_t rawframe_;
		volatile uint16_t offset_;
		volatile uint16_t distance_;
		volatile uint8_t crc_;
};


#endif
