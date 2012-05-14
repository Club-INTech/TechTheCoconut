#ifndef MOTEUR_HPP
#define MOTEUR_HPP

#include "timer.hpp"
#include "safe_enum.hpp"
#include "register.hpp"
#include <libintech/utils.h>
#include "serial/serial_impl.hpp"

struct direction_def
{
	enum type{ RECULER, AVANCER};
};
typedef safe_enum<direction_def> Direction;


template<class Timer, class DirectionRegister>
class Moteur{
	static const uint8_t TIMER_ID = Timer::ID;
	static const uint16_t PRESCALER_VALUE = Timer::PRESCALER_RATIO;
	Timer timer_pwm_;
private:
  void direction(Direction dir){
		if(dir == Direction::AVANCER){
		  //PORTD &=  ~(1 << PORTD4);
		  DirectionRegister::clear();
		}
		else if(dir == Direction::RECULER){
		  //PORTD |=  (1 << PORTD4);
		  DirectionRegister::set();
		}
		//PORTB &=  ~(1 << PORTB0);
  }
  
public:
  Moteur() : maxPWM_(255)
  {
	  Timer::init();
  }
  
  void envoyerPwm(int16_t pwm){	  
	pwm_ = pwm;
    if (pwm>0) {
      direction(Direction::AVANCER);
      Timer::MODE::seuil(min(pwm, maxPWM_)); //Bridage
    }
    else {
      direction(Direction::RECULER);
	  Timer::MODE::seuil(min(-pwm,maxPWM_)); //Bridage
    }
  }
  
  int16_t pwm()
  {
	return pwm_;
  }
  
  void maxPWM(int16_t maxPWM){
	maxPWM_ = maxPWM;
  }
  
  int16_t maxPWM() const{
	return maxPWM_;
  };
  
private:
  int16_t maxPWM_;
  int16_t pwm_;
};


#endif
