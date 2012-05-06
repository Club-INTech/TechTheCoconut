#ifndef PWM_HPP
#define PWM_HPP

#include <stdint.h>
#include <avr/io.h>



template<uint8_t timer_id>
struct ModeCounter{
  static void set();
};

template<>
struct ModeCounter<0>{
  static void seuil(uint16_t seuil){
    OCR0A = seuil;
  }

  static void set(){
    sbi(TIMSK0,TOIE0);
  }
};

template<>
struct ModeCounter<1>{
  static void seuil(uint16_t seuil){
    OCR1A = seuil;
  }

  static void set(){
    sbi(TIMSK1,TOIE1);
  }
};

template<>
struct ModeCounter<2>{
  static void seuil(uint16_t seuil){
    OCR2A = seuil;
  }

  static void set(){
    sbi(TIMSK2,TOIE2);
  }
};

#if	 defined (__AVR_ATmega2560__)\
    || defined (__AVR_ATmega2561__)\
    || defined (__AVR_ATmega1280__)

template<>
struct ModeCounter<3>{
  static void seuil(uint16_t seuil){
    OCR3A = seuil;
  }

  static void set(){
    sbi(TIMSK3,TOIE3);
  }
};

template<>
struct ModeCounter<4>{
  static void seuil(uint16_t seuil){
    OCR4A = seuil;
  }

  static void set(){
    sbi(TIMSK4,TOIE4);
  }
};

template<>
struct ModeCounter<5>{
  static void seuil(uint16_t seuil){
    OCR5A = seuil;
  }

  static void set(){
    sbi(TIMSK5,TOIE5);
  }
};

#endif

template<uint8_t timer_id>
struct ModeFastPwm;

template<>
struct ModeFastPwm<0>{
  static void seuil(uint8_t seuil){
    OCR0A = seuil;
  }
  
  static void set(){
    	// Initialisation pin 12
	DDRD |= ( 1 << PORTD6 );
	cbi(TCCR0A,COM0A0);
	sbi(TCCR0A,COM0A1);
	
	// Fast PWM
	sbi(TCCR0A,WGM00);
	sbi(TCCR0A,WGM01);
	cbi(TCCR0B,WGM02);
  }
};

template<>
struct ModeFastPwm<1>{
  static void seuil(uint8_t seuil){
    OCR1A = seuil;
  }
  static void set(){
    	// Initialisation pin 12
	sbi(DDRB,PORTB1);
	cbi(TCCR1A,COM1A0);
	sbi(TCCR1A,COM1A1);
	
	// Fast PWM
	sbi(TCCR1A,WGM10);
	cbi(TCCR1A,WGM11);
	sbi(TCCR1B,WGM12);
	cbi(TCCR1B,WGM13);
  }
};

template<>
struct ModeFastPwm<2>{
  static void seuil(uint8_t seuil){
    OCR2B = seuil;
  }
  static void set(){
	// Initialisation pin 6
	DDRD |= ( 1 << PORTD3 );
	TCCR2A &= ~( 1 << COM2B0 );
	TCCR2A |= ( 1 << COM2B1 );
	// Fast PWM
	TCCR2A |= ( 1 << WGM20 );
	TCCR2A |= ( 1 << WGM21 );
	TCCR2B &= ~( 1 << WGM22 );
  }
};

#if	 defined (__AVR_ATmega2560__)\
	|| defined (__AVR_ATmega2561__)
	
template<>
struct ModeFastPwm<3>{
  static void seuil(uint8_t seuil){
    OCR3B = seuil;
  }
  static void set(){
	// Initialisation pin 6
	DDRD |= ( 1 << PORTD3 );
	TCCR3A &= ~( 1 << COM3B0 );
	TCCR3A |= ( 1 << COM3B1 );
	// Fast PWM
	TCCR3A |= ( 1 << WGM30 );
	TCCR3A |= ( 1 << WGM31 );
	TCCR3B &= ~( 1 << WGM32 );
  }
};

template<>
struct ModeFastPwm<4>{
  static void seuil(uint8_t seuil){
    OCR4B = seuil;
  }
  static void set(){
        // Initialisation pin 6
        DDRD |= ( 1 << PORTD3 );
        TCCR4A &= ~( 1 << COM4B0 );
        TCCR4A |= ( 1 << COM4B1 );
        // Fast PWM
        TCCR4A |= ( 1 << WGM40 );
        TCCR4A |= ( 1 << WGM41 );
        TCCR4B &= ~( 1 << WGM42 );
  }
};

template<>
struct ModeFastPwm<5>{
  static void seuil(uint8_t seuil){
    OCR5B = seuil;
  }
  static void set(){
        // Initialisation pin 6
        DDRD |= ( 1 << PORTD3 );
        TCCR5A &= ~( 1 << COM5B0 );
        TCCR5A |= ( 1 << COM5B1 );
        // Fast PWM
        TCCR5A |= ( 1 << WGM50 );
        TCCR5A |= ( 1 << WGM51 );
        TCCR5B &= ~( 1 << WGM52 );
  }
};


#endif


#endif
