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

#if	 defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)\
	|| defined (__AVR_ATmega1280__)


template<>
struct TimerRegisters<3, ModeCounter<3> >{
    static uint16_t get_TCNT(){
        return TCNT3;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT3 = new_tcnt;
    }
};

template<>
struct TimerRegisters<4, ModeCounter<4> >{
    static uint16_t get_TCNT(){
        return TCNT4;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT4 = new_tcnt;
    }
};

template<>
struct TimerRegisters<5, ModeCounter<5> >{
    static uint16_t get_TCNT(){
        return TCNT4;
    }

    static void set_TCNT( uint16_t new_tcnt){
       TCNT4 = new_tcnt;
    }
};

#endif

template<uint8_t ID_,template<uint8_t> class MODE_, uint16_t PRESCALER_RATIO_>
class Timer{
	
public:
  static const uint8_t ID = ID_;
  static const uint16_t PRESCALER_RATIO = PRESCALER_RATIO_;
  typedef MODE_<ID_> MODE;
  
private:
  typedef Prescaler<ID,PRESCALER_RATIO> prescaler_;

public:

	static void init(){
		static bool is_init = false;
		if(is_init == false){
			MODE::set();
			prescaler_::set();
			is_init = true;
		}
	}

	
  static inline uint32_t value(){
      return TimerRegisters<ID_,MODE_<ID_> >::get_TCNT();
  }

  static inline void value(uint32_t new_value){
      TimerRegisters<ID_,MODE_<ID_> >::set_TCNT(new_value);
  }
  
  static inline void disable(){
      Prescaler<ID_,0>::set();
  }
  
  static inline void enable(){
      prescaler_::set();
  }
};

#endif
