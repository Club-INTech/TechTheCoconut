#include "moteur.h"

Moteur::Moteur(TimerId id, Prescaler ratio) : timerPwm_(id,ratio) : maxPWM_(1024)
{
}

void Moteur::maxPWM(uint16_t maxPWM)
{
	maxPWM_ = maxPWM;
}

uint16_t Moteur::maxPWM(void)
{
	return maxPWM_;
};

void Moteur::envoyerPwm(int16_t pwm)
{
	if (pwm>0) {
      timerPwm_.direction(Direction::AVANCER);
      timerPwm_.seuil(pwm);
    }
    else {
      timerPwm_.direction(Direction::RECULER);
      timerPwm_.seuil(-pwm);
    }
}
