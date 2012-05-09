#include <libintech/capteur_max.hpp>

ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD2> > ultrason_g;
ultrason< Timer<1,ModeCounter,8>, AVR_PORTD<PORTD3> > ultrason_d;
  
ISR(INT0_vect)
{
	ultrason_g.update();
}

ISR(INT1_vect)
{
	ultrason_d.update();
}