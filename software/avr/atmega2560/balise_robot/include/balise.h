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
	private:
		volatile uint16_t max_counter_;

		typedef Timer<2,ModeFastPwm,1> T_2;
		
		Moteur< T_2, AVR_PORTD<PORTD4> > moteur_;
		Asservissement asservissement_moteur_;

		typedef Timer<0,ModeCounter,8> T_Asservissement;
		
		
	public:
		Balise();
		void asservir(int32_t vitesse_courante);
		void max_counter(uint16_t valeur);
		float getAngle();
};


#endif
