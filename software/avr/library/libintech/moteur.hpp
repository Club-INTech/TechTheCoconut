#ifndef MOTEUR_HPP
#define MOTEUR_HPP

#include "timer.hpp"
#include "safe_enum.hpp"

struct direction_def
{
	enum type{ RECULER, AVANCER};
};
typedef safe_enum<direction_def> Direction;


template<uint8_t TIMER_ID, template<uint8_t> class PWM, uint16_t PRESCALER_VALUE = 1>
class Moteur{
private:
  void direction(Direction dir){
    	if(TIMER_ID==0)
	{
		if(dir == Direction::AVANCER){
		  PORTD &=  ~(1 << PORTD4);
		}
		else if(dir == Direction::RECULER){
		  PORTD |=  (1 << PORTD4);
		}
	}
	else if(TIMER_ID==2)
	{
		if(dir == Direction::AVANCER){
		  PORTB &=  ~(1 << PORTB0);
		}
		else if(dir == Direction::RECULER){
		  PORTB |=  (1 << PORTB0);
		}
	}
  }
  
public:
  void envoyerPwm(int16_t pwm){
    if (pwm>0) {
      direction(Direction::AVANCER);
      timerPwm_.seuil(pwm);
    }
    else {
      direction(Direction::RECULER);
      timerPwm_.seuil(-pwm);
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
  Timer<TIMER_ID, PWM, PRESCALER_VALUE> timerPwm_;
};


#endif