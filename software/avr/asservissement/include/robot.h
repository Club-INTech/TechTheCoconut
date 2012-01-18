#ifndef robot_h
#define robot_h

#include <stdint.h>
#include "usart.h"

#include "i2c.h"
#include "asservissement.h"
#include "timer.hpp"
#include "pwm.hpp"
#include "moteur.hpp"

/**
* Structure principale Robot
*/



struct Robot {
// Par défaut les attributs sont publics dans une struct
	static Robot& Instance();
	void asservir();

	Asservissement translation;
	Asservissement rotation;
	Moteur<0,1,ModeFastPwm> moteurGauche;
	Moteur<2,1,ModeFastPwm> moteurDroit;
	Timer<1,8,ModeCounter> compteur;
	
	/**
	* Setter pour la variable couleur
	*
	* \param unsigned char couleur
	*/
	void couleur(unsigned char);

	/**
	* Getter pour la variable couleur
	*
	* \return unsigned char couleur
	*/
	unsigned char couleur(void);

	/**
	* Setter pour la variable x d'abscisse
	*
	* \param uint16_t abscisse x
	*/
	void x(uint16_t);

	/**
	* Getter pour la variable x d'abscisse
	*
	* \return uint16_t abscisse x
	*/
	uint16_t x(void);
	
	/**
	* Setter pour la variable y d'ordonnée
	*
	* \param uint16_t ordonnée y
	*/
	void y(uint16_t);

	/**
	* Getter pour la variable y d'ordonnée
	*
	* \return uint16_t ordonnée y
	*/
	uint16_t y(void);
	
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
	
private:
	// Un singleton
	Robot();
	Robot(const Robot&);

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
	uint16_t x_;
	
	/**
	* Ordonnée du robot en mm
	*/
	uint16_t y_;
	
	/**
	* Type d'asservissement
	* 
	* @li 'r' pour rotation
	* @li 't' pour translation
	*/
	unsigned char typeAsservissement_;
};

__extension__ typedef int __guard __attribute__((mode (__DI__)));

extern "C" int __cxa_guard_acquire(__guard *);
extern "C" void __cxa_guard_release (__guard *);
extern "C" void __cxa_guard_abort (__guard *);

#endif
