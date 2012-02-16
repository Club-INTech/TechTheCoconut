#ifndef TIMER_HPP
#define TIMER_HPP

#include <stdint.h>
#include <avr/io.h>

#include "utils.h"
#include "prescaler.hpp"
#include "pwm.hpp"
#include "singleton.hpp"

template<uint8_t ID, class Mode>
struct TimerRegisters;

template<>
struct TimerRegisters<0, ModeCounter<0> >{
    static uint16_t get_TCNT(){
        return TCNT0;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT0 = new_tcnt;
    }
};

template<>
struct TimerRegisters<1, ModeCounter<1> >{
    static uint16_t get_TCNT(){
        return TCNT1;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT1 = new_tcnt;
    }
};

template<>
struct TimerRegisters<2, ModeCounter<2> >{
    static uint16_t get_TCNT(){
        return TCNT2;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT2 = new_tcnt;
    }
};

template<uint8_t ID_,template<uint8_t> class MODE_, uint8_t PRESCALER_RATIO_>
class Timer : public Singleton< Timer<ID_, MODE_, PRESCALER_RATIO_> >{
public:
  static const uint8_t ID = ID_;
  static const uint8_t PRESCALER_RATIO = PRESCALER_RATIO_;
  typedef MODE_<ID_> MODE;
private:
  typedef Prescaler<ID,PRESCALER_RATIO> prescaler_;
public:

  Timer(){
    MODE::set();
    prescaler_::set();
  }

  uint16_t value(){
      return TimerRegisters<ID_,MODE_<ID_> >::get_TCNT();
  }

  void value(uint16_t new_value){
      TimerRegisters<ID_,MODE_<ID_> >::set_TCNT(new_value);
  }
};

#endif
