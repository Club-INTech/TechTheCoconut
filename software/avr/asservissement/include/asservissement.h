/**
 * \file asservissement.h
 *
 * Classe gérant les différentes constantes d'asservissement
 */

#ifndef Asservissement_h
#define Asservissement_h

#include <stdint.h>

//Suppression des #define qui ne servent plus

class Asservissement {
	public:

		Asservissement(int16_t kp, int16_t kd=0, int16_t ki=0);
		
		/**
		 * [Ronald:] 
		 * Supprimé la fonction inutile activationKd (il suffit d'avoir kd=0)
		 * Supprimé tout ce qui se rattache à kpVitesse (on n'asservit que en position)
		 * Supprimé méthodes concernant la puissance max
		 * La puissance max des moteurs sera dans la classe Moteur.
		 * Pour vitesse moteur, elle ne devrait jamais servir.
		 * (on asservit en position pas en vitesse)
		 * Suppression de variables publique (erreur,erreurBkp)
		 * Qui devraient être locale aux fonctions (eventuellement static)
		**/
		
		
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
		 * 
		 * Je n'ai pas compris la différence entre le premier paramètre et l'attribut maxPwm_
		 * J'ai aussi renommé la fonction
		 */
		int16_t	pwm(int32_t, int32_t);
		
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
		

		
	private:
		
		/**
		 * Constantes de l'asservissement et du moteur PID (kp;ki;kd)
		 */
		int32_t kp_; 
		int32_t	kd_;
		int32_t	ki_;
};


#endif
