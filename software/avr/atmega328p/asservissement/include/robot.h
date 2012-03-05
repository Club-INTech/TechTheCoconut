#ifndef robot_h
#define robot_h

#include <stdint.h>

#include <avr/io.h>

#include <libintech/asservissement.hpp>
#include <libintech/serial/serial_impl.hpp>
#include <libintech/timer.hpp>
#include <libintech/pwm.hpp>
#include <libintech/moteur.hpp>
#include <libintech/register.hpp>
#include <libintech/singleton.hpp>
/**
* Structure principale Robot
*/

class Robot : public Singleton<Robot>{
// Par défaut les attributs sont publics dans une struct


private:

	//Moteur sur le Timer 2 en FastPWM . Pont en H sur le PORTD4
	typedef Timer<2,ModeFastPwm,1> T_G;
	Moteur< T_G, AVR_PORTD<PORTD4> > moteurGauche;
	
	//Moteur sur le Timer 0 en FastPWM . Pont en H sur le port B0
	typedef Timer<0,ModeFastPwm,1> T_D;
	Moteur<T_D, AVR_PORTB<PORTB0> > moteurDroit;
	
	//Timer 1 en mode compteur, Prescaler de 8
	typedef Timer<1,ModeCounter,8> TimerCounter_t;
	TimerCounter_t compteur;
	
	typedef Serial<0> serial_t_;

	/** Couleur du robot
	* @li 'r' pour Rouge
	* @li 'v' pour Violet
	*/
	unsigned char couleur_;
	
	/**
	* Abscisse du robot en mm
	*/
	float x_;
	
	/**
	* Ordonnée du robot en mm
	*/
	float y_;
	
	/**
	 * angle courant absolu en radian
	*/
	float angle_courant_;
	
	/**
	* constance de conversion de tic en mm
	*/
	float CONVERSION_TIC_MM_;
	
	/**
	* constance de conversion de tic en radian
	*/
	float CONVERSION_TIC_RADIAN_;
	
	/**
	* booléens d'activation de l'asservissement
	*/
	bool etat_rot_;
	bool etat_tra_;
	
	Asservissement translation;
	Asservissement rotation;

public:
	
	Robot();
	
	void asservir(int32_t distance, int32_t angle);
	
	void couleur(unsigned char);

	void updatePosition(int32_t distance, int32_t angle);

	unsigned char couleur(void);
	
	/**
	 * getter pour les coordonnées x,y, en mm
	 */
	
	float x(void);

	float y(void);
	
	float angle_courant(void);
	
	
	/**
	 * setter pour les coordonnées x,y, en mm
	 * \param float coordonnée en mm
	 */
	
	void x(float);
	
	void y(float);
	
	void angle_courant(float);
	
	/**
	 * getter pour l'état activé ou non des asservissement
	 */
	
	bool etat_rot(void);
	bool etat_tra(void);
	
	/**
	 * setter pour l'état activé ou non des asservissement
	 */
	
	
	void etat_rot(bool);
	void etat_tra(bool);
	
	/**
	* Translate le robot
	* 
	* \param float distance de translation en mm
	*/
	void translater(float distance);
	
	/**
	* Tourner le robot
	* 
	* \param float angle de rotation en radians
	*/
	void tourner(float angle);
	
	/**
	* déplace le robot
	* 
	* \param int16_t position sur x à atteindre sur l'aire de jeu, en absolu.
	* \param int16_t position sur y à atteindre sur l'aire de jeu, en absolu.
	*/
	void gotoPos(float x, float y);
	
	void communiquer_pc();
	
	
};

#endif
