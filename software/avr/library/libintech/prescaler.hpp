#ifndef PRESCALER_HPP
#define PRESCALER_HPP

#include <stdint.h>
#include <avr/io.h>

//Prescalers timer 0

template<uint8_t id, uint16_t PrescalerVal>
struct Prescaler{
  static void set();
};

template<>
struct Prescaler<0,0>{
  static void set(){ cbi(TCCR0B,CS02); cbi(TCCR0B,CS01); cbi(TCCR0B,CS00); }
};

template<>
struct Prescaler<0,1>{
  static void set(){ cbi(TCCR0B,CS02); cbi(TCCR0B,CS01); sbi(TCCR0B,CS00); }
};

template<>
struct Prescaler<0,8>{
  static void set(){ cbi(TCCR0B,CS02); sbi(TCCR0B,CS01); cbi(TCCR0B,CS00); }
};

template<>
struct Prescaler<0,64>{
  static void set() { cbi(TCCR0B,CS02); sbi(TCCR0B,CS01); sbi(TCCR0B,CS00); }
};

template<>
struct Prescaler<0,256>{
  static void set() { sbi(TCCR0B,CS02); cbi(TCCR0B,CS01); cbi(TCCR0B,CS00); }
};

template<>
struct Prescaler<0,1024>{
  static void set() { sbi(TCCR0B,CS02); cbi(TCCR0B,CS01); sbi(TCCR0B,CS00); }
};

//Prescalers timer 1

template<>
struct Prescaler<1,0>{
  static void set() { cbi(TCCR1B,CS12); cbi(TCCR1B,CS11); cbi(TCCR1B,CS10); }
};

template<>
struct Prescaler<1,1>{
  static void set() { cbi(TCCR1B,CS12); cbi(TCCR1B,CS11); sbi(TCCR1B,CS10); }
};

template<>
struct Prescaler<1,8>{
  static void set() { cbi(TCCR1B,CS12); sbi(TCCR1B,CS11); cbi(TCCR1B,CS10); }
};

template<>
struct Prescaler<1,64>{
  static void set() { cbi(TCCR1B,CS12); sbi(TCCR1B,CS11); sbi(TCCR1B,CS10); }
};

template<>
struct Prescaler<1,256>{
  static void set() { sbi(TCCR1B,CS12); cbi(TCCR1B,CS11); cbi(TCCR1B,CS10); }
};

template<>
struct Prescaler<1,1024>{
  static void set() { sbi(TCCR1B,CS12); cbi(TCCR1B,CS11); sbi(TCCR1B,CS10); }
};


//Prescalers timer 2

template<>
struct Prescaler<2,0>{
  static void set() { cbi(TCCR2B,CS22); cbi(TCCR2B,CS21); cbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,1>{
  static void set() { cbi(TCCR2B,CS22); cbi(TCCR2B,CS21); sbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,8>{
  static void set() { cbi(TCCR2B,CS22); sbi(TCCR2B,CS21); cbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,32>{
  static void set() { cbi(TCCR2B,CS22); sbi(TCCR2B,CS21); sbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,64>{
  static void set() { sbi(TCCR2B,CS22); cbi(TCCR2B,CS21); cbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,128>{
  static void set() { sbi(TCCR2B,CS22); cbi(TCCR2B,CS21); sbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,256>{
  static void set() { sbi(TCCR2B,CS22); sbi(TCCR2B,CS21); cbi(TCCR2B,CS20); }
};

template<>
struct Prescaler<2,1024>{
  static void set() { sbi(TCCR2B,CS22); sbi(TCCR2B,CS21); sbi(TCCR2B,CS20); }
};

#if	 defined (__AVR_ATmega2560__)\
    || defined (__AVR_ATmega2561__)\
    || defined (__AVR_ATmega1280__)
	
//Prescalers timer 3

template<>
struct Prescaler<3,0>{
  static void set() { cbi(TCCR3B,CS32); cbi(TCCR3B,CS31); cbi(TCCR3B,CS30); }
};

template<>
struct Prescaler<3,1>{
  static void set() { cbi(TCCR3B,CS32); cbi(TCCR3B,CS31); sbi(TCCR3B,CS30); }
};

template<>
struct Prescaler<3,8>{
  static void set() { cbi(TCCR3B,CS32); sbi(TCCR3B,CS31); cbi(TCCR3B,CS30); }
};

template<>
struct Prescaler<3,64>{
  static void set() { cbi(TCCR3B,CS32); sbi(TCCR3B,CS31); sbi(TCCR3B,CS30); }
};

template<>
struct Prescaler<3,256>{
  static void set() { sbi(TCCR3B,CS32); cbi(TCCR3B,CS31); cbi(TCCR3B,CS30); }
};

template<>
struct Prescaler<3,1024>{
  static void set() { sbi(TCCR3B,CS32); cbi(TCCR3B,CS31); sbi(TCCR3B,CS30); }
};

//Prescalers timer 4

template<>
struct Prescaler<4,0>{
  static void set() { cbi(TCCR4B,CS42); cbi(TCCR4B,CS41); cbi(TCCR4B,CS40); }
};

template<>
struct Prescaler<4,1>{
  static void set() { cbi(TCCR4B,CS42); cbi(TCCR4B,CS41); sbi(TCCR4B,CS40); }
};

template<>
struct Prescaler<4,8>{
  static void set() { cbi(TCCR4B,CS42); sbi(TCCR4B,CS41); cbi(TCCR4B,CS40); }
};

template<>
struct Prescaler<4,64>{
  static void set() { cbi(TCCR4B,CS42); sbi(TCCR4B,CS41); sbi(TCCR4B,CS40); }
};

template<>
struct Prescaler<4,256>{
  static void set() { sbi(TCCR4B,CS42); cbi(TCCR4B,CS41); cbi(TCCR4B,CS40); }
};

template<>
struct Prescaler<4,1024>{
  static void set() { sbi(TCCR4B,CS42); cbi(TCCR4B,CS41); sbi(TCCR4B,CS40); }
};

//Prescalers timer 5

template<>
struct Prescaler<5,0>{
  static void set() { cbi(TCCR5B,CS52); cbi(TCCR5B,CS51); cbi(TCCR5B,CS50); }
};

template<>
struct Prescaler<5,1>{
  static void set() { cbi(TCCR5B,CS52); cbi(TCCR5B,CS51); sbi(TCCR5B,CS50); }
};

template<>
struct Prescaler<5,8>{
  static void set() { cbi(TCCR5B,CS52); sbi(TCCR5B,CS51); cbi(TCCR5B,CS50); }
};

template<>
struct Prescaler<5,64>{
  static void set() { cbi(TCCR5B,CS52); sbi(TCCR5B,CS51); sbi(TCCR5B,CS50); }
};

template<>
struct Prescaler<5,256>{
  static void set() { sbi(TCCR5B,CS52); cbi(TCCR5B,CS51); cbi(TCCR5B,CS50); }
};

template<>
struct Prescaler<5,1024>{
  static void set() { sbi(TCCR5B,CS52); cbi(TCCR5B,CS51); sbi(TCCR5B,CS50); }
};

#endif

#endif