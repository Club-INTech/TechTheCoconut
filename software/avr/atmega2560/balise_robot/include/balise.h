/**
 * \file balise.h
 *
 * Classe représentant la balise
 */

#ifndef Balise_h
#define Balise_h

#include <stdint.h>
#include <libintech/singleton.hpp>
#include <libintech/moteur.hpp>
#include <libintech/asservissement.hpp>
#include "utils.h"

class Balise : public Singleton<Balise>{
	public:
		typedef Serial<0> serial_pc;
		typedef Serial<1> serial_radio;
		typedef Timer<3,ModeCounter,64> T_TopTour;
		typedef Timer<1,ModeCounter,64> T_Asservissement;
	private:
		volatile uint32_t max_counter_;
// 		volatile uint32_t toptour_;
		typedef Timer<2,ModeFastPwm,1> T_2;
		Moteur< T_2, AVR_PORTD<PORTD4> > moteur_;
		Asservissement asservissement_moteur_;
		
	public:
		Balise();
		void asservir(int32_t vitesse_courante);
		void max_counter(uint16_t valeur);
		uint16_t max_counter();
		uint32_t  getAngle(uint16_t offset);
// 		void incremente_toptour();
// 		void reset_toptour();
// 		uint16_t toptour();
		
};


#endif
