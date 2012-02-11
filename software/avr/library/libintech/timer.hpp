#ifndef TIMER_HPP
#define TIMER_HPP

#include <stdint.h>
#include <avr/io.h>

#include "utils.h"
#include "prescaler.hpp"

template<uint8_t ID_,template<uint8_t> class MODE_, uint8_t PRESCALER_RATIO_>
class Timer{
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
  
  void seuil(uint16_t seuil){
    MODE::seuil(seuil);
  }
};
#endif
