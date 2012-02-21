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

		int32_t	pwm(int32_t positionReelle, int32_t eps = 0)
		{
			enm2_ = enm1_;
			enm1_ = en_;
			en_=consigne_ - positionReelle;
			
// 			if (abs(en_)<eps && abs(enm1_)<eps && abs(enm2_)<eps)
// 			{
// 				enm2_ = 0;
// 				enm1_ = 0;
// 				en_ = 0;
// 				pwmCourant_=0;
// 			}
// 			
			pwmCourant_+=kp_*(en_ - enm1_) + ki_*en_ + kd_*(en_ - 2*enm1_ + enm2_);
			/*
			if(pwmCourant_ > valeur_bridage_)
				return  valeur_bridage_;
			else if (pwmCourant_ < -valeur_bridage_)
				return -valeur_bridage_;
			*/
			return pwmCourant_;
			
		}
		
	
		void ki(float ki)
		{
			ki_ = ki;
		}

		uint16_t ki(void)
		{
			return ki_;
		}

		void kd(float kd)
		{
			kd_ = kd;
		}

		uint16_t kd(void)
		{
			return kd_;
		}

		void kp(float kp)
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
			return en_;
		}
		int8_t valeur_bridage(void){
			return valeur_bridage_;
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
