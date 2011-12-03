#ifndef Moteur_h
#define Moteur_h

#include "timer.h"

class Moteur{
public:
  Moteur(TimerId id, Prescaler ratio);
  void envoyerPwm(int16_t pwm);
  void maxPWM(int16_t);
  int16_t maxPWM();
private:
  Timer timerPwm_;
  uint16_t maxPWM_;
};

#endif
