#include <libintech/capteur_srf05.hpp>

typedef Serial<0> serial_t_;
typedef Timer<1,ModeCounter,64> timerCapteurSRF;

capteur_srf05<timerCapteurSRF, serial_t_> capteur_srf05_t_;


template <>
volatile bool capteur_srf05<timerCapteurSRF, serial_t_>::busy = false;

/** Interruption pour un changement d'état sur la pin.
 */
ISR(PCINT2_vect)
{
   capteur_srf05_t_.interruption();
}

