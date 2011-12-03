#ifndef Moteur_h
#define Moteur_h

#include "timer.h"

class Moteur{
public:
  Moteur(TimerId id, Prescaler ratio);
  void envoyerPwm(int16_t pwm);
private:
  Timer timerPwm_;
};

#endif
