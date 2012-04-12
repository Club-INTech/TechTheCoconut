#ifndef ULTRASON_HPP
#define ULTRASON_HPP

#include <libintech/timer.hpp>
#include <libintech/register.hpp>
#include <libintech/ring_buffer.hpp>

int compare (const void * a, const void * b);
  
template<class Timer, class Pin>
class ultrason
{
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
  
  uint16_t mediane(){
    qsort(mesures_.data(),mesures_.size(),sizeof(uint16_t),compare);
    return mesures_.data()[mesures_.size()/2];
  }
  
};

extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
extern ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;

#endif