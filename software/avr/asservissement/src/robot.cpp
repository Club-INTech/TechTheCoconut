
#include "robot.h"
#include "i2c.h"

Robot::Robot() : moteurGauche_(TimerId::T0,Prescaler::NO_PRESCAL)
				, moteurDroit_(TimerId::T2,Prescaler::NO_PRESCAL)
				, compteur_(TimerId::T1,Prescaler::P8)
{ 
	uart_init();
	printlnString("debut");
}

void Robot::asservir()
{
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
    get_all(infos);
    int16_t pwmTranslation = translation_.pwm(infos[0]);
    int16_t pwmRotation = rotation_.pwm(infos[1]);
    moteurGauche_.envoyerPwm(pwmTranslation - pwmRotation);
    moteurDroit_.envoyerPwm(pwmTranslation + pwmRotation);
}
