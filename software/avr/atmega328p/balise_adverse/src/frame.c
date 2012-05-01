#include "frame.h"

Frame makeFrame(uint16_t distance, uint16_t offset)
{
	Frame frame=0;
	Crc crc=0;
	Data data = distance;
	
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

void sendFrame(Frame frame)
{
	Serial<0>::print(frame);
}
