#ifndef ULTRASON_HPP
#define ULTRASON_HPP

#include <libintech/timer.hpp>
#include <libintech/register.hpp>
#include <libintech/ring_buffer.hpp>
#include <libintech/algorithm.hpp>
  
template<class Timer, class Pin>
class ultrason
{
  typedef uint16_t mesure_t;
  ring_buffer<uint16_t, 3> mesures_;
  uint16_t derniere_valeur_;

public:
  ultrason(){
    Timer::init();
  }
  
  void update(){
    if(Pin::read()){
		derniere_valeur_ = Timer::value();
    }else{//Front descendant
	// prescaler/fcpu*inchToCm/tempsParInch
	if(Timer::value() <derniere_valeur_)
	  mesures_.append((Timer::value() + 65536 - derniere_valeur_  )*0.0884353741496);
	else
	  mesures_.append((Timer::value() - derniere_valeur_ )*0.0884353741496);
    }
  }
  
  uint16_t value(){
    return mediane(mesures_);
  }
  
};

#endif