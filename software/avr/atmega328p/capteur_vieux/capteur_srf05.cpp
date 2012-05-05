#include <libintech/capteur_vieux.hpp>

typedef Serial<0> serial_t_;
typedef Timer<1,ModeCounter,256> timerCapteur;

capteur_srf05<timerCapteur> capteur_srf05_t_;


template <>
volatile bool capteur_srf05<timerCapteur>::busy = false;

/** Interruption pour un changement d'état sur la pin.
 */
ISR(PCINT2_vect)
{
   capteur_srf05_t_.interruption();
}

