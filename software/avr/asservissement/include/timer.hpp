#ifndef TIMER_HPP
#define TIMER_HPP

#include "utils.h"
#include "prescaler.hpp"

template<uint8_t ID,template<uint8_t> class MODE, uint8_t PRESCALER_RATIO>
class Timer{
  typedef Prescaler<ID,PRESCALER_RATIO> prescaler_;
  typedef MODE<ID> mode_;
public:
  Timer(){
    mode_::set();
    prescaler_::set();
  }
  
  void seuil(uint16_t seuil){
    mode_::seuil(seuil);
  }
};
#endif