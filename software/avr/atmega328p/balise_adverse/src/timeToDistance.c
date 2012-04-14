#include "timeToDistance.h"

static const uint16_t delta_t[] = { DELTA_T };
static const uint16_t distance[] = { DISTANCE };

uint16_t getDistance(uint16_t delta)
{
	unsigned int i=0;

	for(i=0;i<TABLE_LENGTH;++i)
	{
		if(delta<delta_t[i])
			break;
	}

	return linearReg(delta,delta_t[i-1],distance[i-1],delta_t[i],distance[i]);
}

inline uint16_t linearReg(int32_t x, int32_t x1, int32_t y1, int32_t x2, int32_t y2)
{
	return (y2-y1)*(x-x1)/(x2-x1)+y1;
}
