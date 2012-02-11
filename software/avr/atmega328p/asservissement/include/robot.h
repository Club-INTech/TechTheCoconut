#ifndef robot_h
#define robot_h

#include <stdint.h>

#include <avr/io.h>

#include "asservissement.h"
#include <libintech/forwards_serial.h>
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
	
	//Moteur sur le Timer 0 en FastPWM . Pont en H sur le PORTD4
	typedef Timer<0,ModeFastPwm,1> T_0;
	Moteur< T_0, AVR_PORTD<PORTD4> > moteurGauche;
	//Moteur sur le Timer 2 en FastPWM . Pont en H sur le port B0
	Moteur<Timer<2,ModeFastPwm,1>, AVR_PORTB<PORTB0> > moteurDroit;
	//Timer 1 en mode compteur, Prescaler de 8
	Timer<1,ModeCounter,8> compteur;
	Serial<0> & serial_;

		/**
	* Couleur du robot
	* 
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

	Asservissement translation;
	Asservissement rotation;

public:
	
	Robot();
	
	void asservir(int32_t distance, int32_t angle);
	
	/**
	* Setter pour la variable couleur
	*
	* \param unsigned char couleur
	*/
	void couleur(unsigned char);

	void updatePosition(int32_t distance, int32_t angle);
	/**
	* Getter pour la variable couleur
	*
	* \return unsigned char couleur
	*/

	unsigned char couleur(void);
	/**
	* Getter pour la variable x d'abscisse
	*
	* \return uint16_t abscisse x
	*/
	int16_t x(void);

	/**
	* Getter pour la variable y d'ordonnée
	*
	* \return uint16_t ordonnée y
	*/
	int16_t y(void);
	
	/**
	* Setter pour la variable typeAsservissement
	*
	* \param unsigned char typeAsservissement
	*/
	void typeAsservissement(unsigned char);

	/**
	* Getter pour la variable typeAsservissement
	*
	* \return unsigned char typeAsservissement
	*/
	unsigned char typeAsservissement(void);
	
	/**
	* TODO
	* Translate le robot
	* 
	* \param int32_t distance de translation en mm (négative pour reculer, positive pour avancer)
	* \return bool true si réussi, false si échec
	*/
	bool translater(uint16_t distance);
	
	/**
	* TODO
	* Tourner le robot
	* 
	* \param int32_t angle de rotation en radians*10000 (positif pour anti-horaire = trigo, négatif pour horaire)
	* \return bool true si réussi, false si échec
	*/
	bool tourner(uint16_t angle);
	
	void communiquer_pc();
	
};

#endif
