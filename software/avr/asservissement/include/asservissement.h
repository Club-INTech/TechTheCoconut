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
		 * Supprimé tout ce qui se rattache à kpVitesse. (L'année dernière il y a eu une tentative ratée d'asservissement en vitesse que nous ne réintérons pas cette année. Désolé de ne pas l'avoir précisé)
		 * Bougé les méthodes concernant la puissance max dans la classe Moteur
		 * Rajouté attribut vitesse dans les classes Rotation, Translation plutôt que Asservissement
		 * les variables ereurs,erreursBkp... ont plus de sens en local dans la méthode asservir()
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
