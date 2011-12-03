#include "moteur.h"

Moteur::Moteur(TimerId id, Prescaler ratio) : timerPwm_(id,ratio)
{
}

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
