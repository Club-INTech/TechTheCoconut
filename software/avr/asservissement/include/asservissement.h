/**
 * \file asservissement.h
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>

// Constante de l'asservissement
#define KP		30
#define VMAX	50000
#define ACC		22
#define KD		35

#define TRIGGER_BLOCAGE	15

class Asservissement {
	public:
		Asservissement();
		
		/**
		 * Getter pour la consigne actuelle
		 * 
		 * \return unsigned char consigneActuelle
		 */
		unsigned char recupererConsigne();
		
		//----
		void stop();
		
		int32_t	calculePwm(int32_t,int32_t);

		void changekp(uint16_t);  /// 
		void setActivationKd(unsigned char);
		void changeKd(uint16_t);
		void changeKi(uint16_t);
		void changeKpVitesse(uint16_t);

		// void changeAcc(int32_t); not use
		void changeVmax(int32_t);
		void changePWM(int);

		void reset();
		
		void setVitesse(int32_t);	
		
		

		// Constantes de l'asservissement et du moteur	
		int32_t kp; 
		int32_t	kd;
		int32_t	ki;
		int32_t	kpVitesse;

		int32_t vMax;
		int32_t maxPWM; 
		

		// erreur
		int32_t	erreur;
		int32_t	erreurBkp;
		int32_t	integraleErreur;

		unsigned char activationKd;


		// Vaut 1 ou -1 si le moteur est bloqué
		int16_t blocageDetecte;
		int blocageTemp;

		// Vitesse du robot;
		int32_t	vitesse;
		
	private:
		/**
		 * Consigne actuelle donnée à par l'asservissement à la liaison série
		 */
		unsigned char consigneActuelle;
};


#endif
