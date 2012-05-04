#include "frame.h"

int32_t makeFrame(uint16_t distance, uint16_t offset)
{
	int32_t frame=0;
	uint8_t crc=0;
	int32_t data = distance;
	
	if(offset > 4096 || distance > 4096)
	  return 0;
	frame+=(((uint32_t) offset) << 8);
	frame+=(((uint32_t) distance) << 20);
	
	//Calcul du CRC
	crc = crc8(frame);
	//On ajoute le CRC
	frame += crc;

	return frame;
}

void sendFrame(int32_t frame)
{
	Serial<0>::print(frame);
}
