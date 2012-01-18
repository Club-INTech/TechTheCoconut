#ifndef PWM_HPP
#define PWM_HPP

template<uint8_t timer_id>
struct ModeFastPwm{
  static const uint8_t seuil;
  static void set();
};

template<>
struct ModeFastPwm<0>{
  static const uint8_t top = OCR0A;
  static void set(){
    	// Initialisation pin 12
	DDRD |= ( 1 << PORTD6 );
	cbi(TCCR0A,COM0A0);
	sbi(TCCR0A,COM0A1);
	
	// Fast PWM
	sbi(TCCR0A,WGM00)
	sbi(TCCR0A,WGM01);
	cbi(TCCR0B,WGM02);
  }
};

template<>
struct ModeFastPwm<1>{
  static const uint8_t top = OCR1A;
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
  static const uint8_t top = OCR2B;
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

template<uint8_t timer_id>
struct ModeCounter{
  static void set();
};

template<>
struct ModeCounter<0>{
  static const uint8_t top = OCR0A;
  static void set(){
    sbi(TIMSK0,TOIE0);
  }
};

template<>
struct ModeCounter<1>{
  static const uint8_t top = OCR1A;
  static void set(){
    sbi(TIMSK1,TOIE1);
  }
};

struct ModeCounter<2>{
  static const uint8_t top = OCR2A;
  static void set(){
    sbi(TIMSK2,TOIE2);
  }
};

#endif