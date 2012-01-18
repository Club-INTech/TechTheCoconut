#ifndef Moteur_h
#define Moteur_h

#include "timer.h"

class Moteur{
public:
  template<uint8_t timer_id, uint16_t prescalerVal>
  Moteur(Prescaler<timer_id,prescalerVal> prescaler);
  void envoyerPwm(int16_t pwm);
  void maxPWM(uint16_t);
  uint16_t maxPWM();
private:
  Timer timerPwm_;
  uint16_t maxPWM_;
};

#endif
