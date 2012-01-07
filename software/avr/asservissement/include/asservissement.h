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

		Asservissement(uint16_t kp, uint16_t kd, uint16_t ki);


		/**
		* \brief Arret
		*
		* Arrete le moteur progressivement
		*/
		void stop();

		/**
		* Calcule de la puissance moteur
		*
		* \param int32_t positionRelle
		* \return int32_t pwm puissance à appliquer
		*/
		int16_t	pwm(int32_t);

		/**
		* accesseurs des variables PID (kp,ki,kp)
		*/

		/**
		* Setter pour la variable intégral ki
		*
		* \param uint16_t kiDonne
		*/
		void ki(uint16_t);

		/**
		* Getter pour la variable intégral ki
		*
		* \return uint16_t variable intégral ki
		*/
		uint16_t ki(void);

		/**
		* Setter pour la variable dérivé kd
		*
		* \param uint16_t kdDonne
		*/
		void kd(uint16_t);

		/**
		* Getter pour la variable dérivé kd
		*
		* \return uint16_t variable dérivé kd
		*/
		uint16_t kd(void);


		/**
		* Setter pour la variable proportionnel kp
		*
		* \param uint16_t kpDonne
		*/
		void kp(uint16_t);

		/**
		* Getter pour la variable proportionnel kp
		*
		* \return uint16_t variable proportionnel kp
		*/
		uint16_t kp(void);

		/**
		* Setter pour la variable de PWM Max
		*
		* \param uint16_t pwmMax
		*/
		void pwmMax(uint16_t);

		/**
		* Getter pour la variable de PWM Max
		*
		* \return uint16_t PWM Maximum
		*/
		uint16_t pwmMax(void);
		
		/**
		* Getter pour la consigne courante
		*
		* \return int32_t consigne
		*/
		int32_t consigne();

		/**
		* Setter pour la consigne courante
		*
		*/
		void consigne(int32_t);

		/**
		* Getter pour la vitesse
		*
		* \return int32_t consigne
		*/
		int32_t vitesse();

		/**
		* Setter pour la vitesse
		*
		*/
		void vitesse(int32_t);

		/**
		* Remet à zéro l'asservissement en rotation en réinitialisant les données
		* Enlevé la valeur de retour car ca ne devrait jamais rater. Et si jamais ça rate, on aura aucun moyen de faire remonter ça dans le code.
		*/
		void reset();
		
		/**
		* TODO
		* 
		* Vide la liste des consignes
		*/
		void resetConsignes();

	private:

		/**
		* Constantes de l'asservissement et du moteur PID (kp;ki;kd)
		*/
		float kp_;
		float kd_;
		float ki_;
		
		float en_;
		float enm1_;
		float enm2_;
		
		int16_t pwmCourant_;
		uint16_t pwmMax_;

		int32_t consigne_;
		int32_t vitesse_;
};


#endif
