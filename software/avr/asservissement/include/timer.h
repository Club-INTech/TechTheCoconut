#ifndef Timer_h
#define Timer_h

#include <stdint.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include "safe_enum.hpp"

/**
 * Les timers disponibles sur le microcontrôleur.
 **/
struct TimerId_def
{
	enum type{ T0, T1, T2};
};
typedef safe_enum<TimerId_def> TimerId;


struct prescaler_def
{
	enum type{ NO_PRESCAL = (1 << CS00), P8 = (1 << CS11), P64 = ((1 << CS11) | (1 << CS10 ))};
};
typedef safe_enum<prescaler_def,uint8_t> Prescaler;

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
	Timer(TimerId id, Prescaler ratio);
	void direction(Direction dir);
	void seuil(uint16_t seuil);
	
private:
	TimerId id_;
};



 
#endif
