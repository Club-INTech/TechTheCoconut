/**
 * \file asservissement.h
 *
 * Classe gérant les différentes constantes d'asservissement
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>

/**
  * Constante de puissance moteur
  */
#define PWM_MAX 255
  
/**
  * Constante de d'asservissement
  */
#define KP		30
#define VMAX	50000
#define ACC		22
#define KD		35

#define TRIGGER_BLOCAGE	15

class Asservissement {
	public:
		/**
		 * Constructeur
		 */
		Asservissement();
		
		/**
		 * Getter pour la consigne actuelle
		 * 
		 * \return unsigned char consigneActuelle
		 */
		unsigned char recupererConsigne();
		
		/**
		 * \brief Arret
		 *
		 * Arrete le moteur progressivement
		 */
		void stop();
		
		/**
		 * Calcule de la puissance moteur
		 *
		 * \param int32_t puissance moteur ,  int32_t positionRelle 
		 * \return int32_t pwm puissance à appliquer
		 */
		int32_t	calculePwm(int32_t,int32_t);
		
		/**
		 * accesseurs des variables PID (kp,ki,kp)
		 */
		 
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
		 * Setter activation du correcteur proportionnel
		 * 
		 * \param unsigned char etatDonne 1 actif ou 0 inactif
		 */
		void activationKd(unsigned char);
		
		/**
		 * Setter pour la variable vitesse 
		 * 
		 * \param uint16_t kpVitesseDonne
		 */
		void kpVitesse(uint16_t);
		
		/**
		 * Getter pour la variable proportionnel kp
		 * 
		 * \return uint16_t variable kpvitesse
		 */
		uint16_t kpVitesse(void);
		
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
		 * Setter pour la variable vmax vitesse max
		 * 
		 * \param int32_t vMaxDonne vitesse max
		 */
		void vMax(int32_t);
		
		/**
		 * Getter pour la variable vmax vitesse max
		 * 
		 * \return int32_t vMax vitesse max
		 */
		int32_t vMax(void);
		
		/**
		 * Setter pour la puissance max du moteur
		 * 
		 * \param int16_t ou int maxPwmDonne puissance max du moteur
		 */
		void pwm(int);
		
		/**
		 * Getter puissance max du moteur
		 * 
		 * \return int16_t ou int maxPWM puissance max du moteur
		 */
		int pwm(void);
		
		/**
		 * Setter vitesse moteur
		 * 
		 * \param int16_t vitesseDonnee vitesse moteur
		 */
		void vitesse(int32_t);	
		
		/**
		 * Getter vitesse moteur
		 * 
		 * \return int16_t vitesse   vitesse moteur
		 */
		int32_t vitesse(void);	

		// erreur
		int32_t	erreur;
		int32_t	erreurBkp;
		int32_t	integraleErreur;

		unsigned char activationKd_;

		// Vaut 1 ou -1 si le moteur est bloqué
		int16_t blocageDetecte;
		int blocageTemp;
		
	private:
		/**
		 * Consigne actuelle donnée à par l'asservissement à la liaison série
		 */
		unsigned char consigneActuelle;
		
		/**
		 * Constantes de l'asservissement et du moteur PID (kp;ki;kd)
		 */
		int32_t kp_; 
		int32_t	kd_;
		int32_t	ki_;
		int32_t	kpVitesse_;
		
		/**
		 * Variables gérant la vitesse & la puissance moteur
		 */
		int32_t vMax_;
		int32_t maxPWM_; 
		int32_t	vitesse_;
};


#endif
