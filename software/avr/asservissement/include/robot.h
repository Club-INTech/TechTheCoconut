#ifndef robot_h
#define robot_h

#include <stdint.h>
#include "usart.h"

#include "i2c.h"
#include "rotation.h"
#include "translation.h"
#include "moteur.h"
#include "timer.h"

/**
 * Structure principale Robot
 */
class Robot {
public:
    static Robot& Instance();
	void asservir();
private:
	Robot();
	Robot(const Robot&);
	Translation translation_; 
	Rotation rotation_;
	Moteur moteurGauche_;
	Moteur moteurDroit_;
	Timer compteur_;
};

__extension__ typedef int __guard __attribute__((mode (__DI__))); 

extern "C" int __cxa_guard_acquire(__guard *); 
extern "C" void __cxa_guard_release (__guard *); 
extern "C" void __cxa_guard_abort (__guard *); 

#endif
