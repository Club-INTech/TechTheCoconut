/**
 * \file asservissement.h
 *
 * Classe gérant les différentes constantes d'asservissement
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>

class Asservissement {
	public:

		Asservissement(float kp,float kd,float ki) : kp_(kp), kd_(kd), ki_(ki) { }

		int16_t	pwm(int32_t positionReelle)
		{
			static float en_ = 0;
			static float enm1_ = 0;
			static float enm2_ = 0;
			enm2_ = enm1_;
			enm1_ = en_;
			en_=consigne_ - positionReelle;
			pwmCourant_+=static_cast<int16_t>(kp_*(en_ - enm1_) + ki_*en_ + kd_*(en_ - 2*enm1_ + enm2_));
			if(pwmCourant_ > (int16_t)pwmMax_){
				return pwmMax_;
			}
			else if(pwmCourant_ < (-1)*(int16_t)pwmMax_){
				return (-1)*pwmMax_;
			}
			return pwmCourant_;
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

		void pwmMax(uint16_t pwmMax)
		{
			pwmMax_ = pwmMax;
		}

		uint16_t pwmMax(void)
		{
			return pwmMax_;
		}

		int32_t consigne()
		{
			return consigne_;
		}

		void consigne(int32_t consigne)
		{
			consigne_ = consigne;
		}


	private:

		float kp_;
		float kd_;
		float ki_;
		
		int16_t pwmCourant_;
		uint16_t pwmMax_;

		int32_t consigne_;
};


#endif
