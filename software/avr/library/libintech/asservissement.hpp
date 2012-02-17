/**
 * \file asservissement.h
 *
 * Classe gérant les différentes constantes d'asservissement
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>
#include <libintech/utils.h>

class Asservissement {
	
	public:

		Asservissement(float kp,float kd,float ki) : kp_(kp), kd_(kd), ki_(ki), valeur_bridage_(255){ }

		int32_t	pwm(int32_t positionReelle)
		{
			enm2_ = enm1_;
			enm1_ = en_;
			en_=consigne_ - positionReelle;
			pwmCourant_=kp_*en_+ kd_*(en_ - enm1_);
// 			if(pwmCourant_ > 0)
// 				pwmCourant_ = min(pwmCourant_,valeur_bridage_);
// 			else
// 				pwmCourant_ = max(pwmCourant_, -valeur_bridage_);
			return pwmCourant_;
// 			if(pwmCourant_>0)
// 				return min(pwmCourant_, (int16_t)valeur_bridage_);
// 			else
// 				return max(pwmCourant_, -(int16_t)valeur_bridage_);
		}

		void ki(uint16_t ki)
		{
			ki_ = ki;
		}

		uint16_t ki(void)
		{
			return ki_;
		}

		void kd(uint16_t kd)
		{
			kd_ = kd;
		}

		uint16_t kd(void)
		{
			return kd_;
		}

		void kp(uint16_t kp)
		{
			kp_ = kp;
		}

		uint16_t kp(void)
		{
			return kp_;
		}

		int32_t consigne()
		{
			return consigne_;
		}

		void consigne(int32_t consigne)
		{
			consigne_ = consigne;
		}

		float erreur()
		{
			return en_ - enm1_;
		}
		
		void valeur_bridage(int8_t new_val){
			valeur_bridage_  = new_val;
		}

	private:

		float kp_;
		float kd_;
		float ki_;

		int16_t valeur_bridage_;

		float pwmCourant_;
		float en_;
		float enm1_;
		float enm2_;
		
		int32_t consigne_;
};


#endif
