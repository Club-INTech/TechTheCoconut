
#include "robot.h"
#include "twi_master.h"

Robot::Robot() : moteurGauche_(TimerId::T0,Prescaler::NO_PRESCAL)
				, moteurDroit_(TimerId::T2,Prescaler::NO_PRESCAL)
				, compteur_(TimerId::T1,Prescaler::P8)
{ 
    TWI_init();
	uart_init();
	printlnString("debut");
}

int __cxa_guard_acquire(__guard *g) {return !*(char *)(g);}; 
void __cxa_guard_release (__guard *g) {*(char *)g = 1;}; 
void __cxa_guard_abort (__guard *) {}; 

Robot& Robot::Instance()
{
	static Robot robot;
	return robot;
}

void Robot::asservir()
{
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
    get_all(infos);
    int16_t pwmTranslation = translation_.pwm(infos[0]);
    int16_t pwmRotation = rotation_.pwm(infos[1]);
    moteurDroit_.envoyerPwm(pwmTranslation - pwmRotation);
    moteurGauche_.envoyerPwm(pwmTranslation + pwmRotation);
}
