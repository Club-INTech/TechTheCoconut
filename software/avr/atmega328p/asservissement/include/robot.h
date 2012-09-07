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
	
	//kit pour borne d'arcade
	bool BASCULE_;
	int32_t pwmG_;
	int32_t pwmD_;
	
	unsigned char couleur_;
	float x_;
	float y_;
	float angle_serie_;
	float angle_origine_;
	
	bool etat_rot_;
	bool etat_tra_;
	volatile bool est_bloque_;
	
	int32_t mesure_distance_;
	int32_t mesure_angle_;
	
	Asservissement translation;
	Asservissement rotation;

	float CONVERSION_TIC_MM_;
	float CONVERSION_TIC_RADIAN_;
	
public:
	
	Robot();
	
	//kit pour borne d'arcade
	void bandeArcade();
	bool BASCULE();
	
	//gestion des mesures courantes
	void mesure_angle(int32_t); 
	void mesure_distance(int32_t); 
	
	void changer_orientation(float new_angle);
	
	void changerVitesseTra1();
	void changerVitesseTra2();
	void changerVitesseTra3();
	void changerVitesseRot1();
	void changerVitesseRot2();
	void changerVitesseRot3();
	
	void asservir();
	void update_position();
	void communiquer_pc();
	
	int32_t angle_optimal(int32_t angle, int32_t angleBkp);
	
	void tourner(float angle);
	void translater(float distance);

	void stopper();
	bool est_stoppe();
	void gestion_blocage();
	
	void recalage(void);
	void translater_bloc(float distance);
	void tourner_bloc(float angle);
};

#endif
