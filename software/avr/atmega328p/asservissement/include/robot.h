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

//structure sauvegardant les valeurs courantes de rotation et translation, en tics.
struct Mesure {
	int32_t angle;
	int32_t distance;
};

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
	
	unsigned char couleur_;
	float x_;
	float y_;
	float angle_courant_;
	
	float CONVERSION_TIC_MM_;
	float CONVERSION_TIC_RADIAN_;
	
	bool etat_rot_;
	bool etat_tra_;
	
	int32_t consigne_tra_;
	
	bool rotation_en_cours_;
	
	bool translation_attendue_;
	bool rotation_attendue_;
	bool goto_attendu_;
	
	bool demande_stop_;
	
	Mesure mesure_;
	
	Asservissement translation;
	Asservissement rotation;

public:
	
	Robot();
	
	void couleur(unsigned char);
	unsigned char couleur(void);
	void x(float);
	float x(void);
	void y(float);
	float y(void);
	void angle_courant(float);
	float angle_courant(void);
	void mesure(Mesure); 
	Mesure mesure(void);
	
	void asservir(int32_t distance, int32_t angle);
	void updatePosition(int32_t distance, int32_t angle);
	void communiquer_pc();
	
	void gotoPos(float x, float y);
	void debut_tourner(float angle);
	void fin_tourner(void);
	void debut_translater(float distance);
	void fin_translater(void);
	
	void stopper(int32_t distance);
	void atteinteConsignes(void);
	void gestionStoppage(int32_t distance, int32_t angle);
};

#endif
