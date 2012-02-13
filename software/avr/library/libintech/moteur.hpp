#ifndef MOTEUR_HPP
#define MOTEUR_HPP

#include "timer.hpp"
#include "safe_enum.hpp"
#include "register.hpp"
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
  void envoyerPwm(int16_t pwm){
    if (pwm>0) {
      direction(Direction::AVANCER);
      Timer::MODE::seuil(pwm);
    }
    else {
      direction(Direction::RECULER);
      Timer::MODE::seuil(-pwm);
    }
  }
  
  void maxPWM(uint16_t maxPWM){
	maxPWM_ = maxPWM;
  }
  
  uint16_t maxPWM() const{
	return maxPWM_;
  };
  
private:
  uint16_t maxPWM_;
};


#endif
