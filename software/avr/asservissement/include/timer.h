#ifndef Timer_h
#define Timer_h

#include <stdint.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include "safe_enum.hpp"

/**
 * Les timers disponibles sur le microcontrôleur.
 **/





/**
 * Les Directions de déplacement
 **/
struct direction_def
{
	enum type{ RECULER, AVANCER};
};
typedef safe_enum<direction_def> Direction;

class Timer
{
public:
	template<uint8_t id, uint16_t PrescalerVal>
	Timer(Prescaler<id,PrescalerVal> prescal);
	void direction(Direction dir);
	void seuil(uint16_t seuil);
	
private:
	Timer(const Timer&);
	
	const uint8_t id_;
};



 
#endif
