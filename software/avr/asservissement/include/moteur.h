#ifndef Moteur_h
#define Moteur_h

#include "timer.h"

class Moteur{
public:
  Moteur(TimerId id, Prescaler ratio);
  void envoyerPwm(int16_t pwm);
  void maxPWM(uint16_t);
  uint16_t maxPWM();
private:
  Timer timerPwm_;
  uint16_t maxPWM_;
};

#endif
