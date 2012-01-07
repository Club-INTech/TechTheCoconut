
#include "robot.h"
#include "twi_master.h"

// Constructeur avec assignation des attributs
Robot::Robot() : translation(0.2,0.2,0.2),
				rotation(0.2,0.2,0.2),
				moteurGauche(TimerId::T0,Prescaler::NO_PRESCAL),
				moteurDroit(TimerId::T2,Prescaler::NO_PRESCAL),
				compteur(TimerId::T1,Prescaler::P8),
				couleur_('r'),
				x_(0),
				y_(0),
				typeAsservissement_('t')
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
	int16_t pwmTranslation = translation.pwm(infos[0]);
	int16_t pwmRotation = rotation.pwm(infos[1]);
printlnLong(pwmTranslation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
}

void Robot::couleur(unsigned char couleur)
{
	if (couleur == 'r' || couleur == 'v')
		couleur_ = couleur;
}

unsigned char Robot::couleur(void)
{
return couleur_;
}

void Robot::x(uint16_t x)
{
	x_ = x;
}

uint16_t Robot::x(void)
{
return x_;
}

void Robot::y(uint16_t y)
{
	y_ = y;
}

uint16_t Robot::y(void)
{
return y_;
}

void Robot::typeAsservissement(unsigned char typeAsservissement)
{
	if (typeAsservissement == 'r' || typeAsservissement == 't')
		typeAsservissement_ = typeAsservissement;
}

unsigned char Robot::typeAsservissement(void)
{
return typeAsservissement_;
}

bool Robot::translater(uint16_t distance)
{
	return true;
}

bool Robot::tourner(uint16_t angle)
{
	return true;
}
