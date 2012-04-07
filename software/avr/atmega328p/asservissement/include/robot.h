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
	
	unsigned char couleur_;
	float x_;
	float y_;
	float angle_serie_;
	float angle_origine_;
	void changer_orientation(float new_angle);
	
	//booléens pour envoyer un acquittement différent sur deux
	bool bascule_goto_;
	bool bascule_tra_;
	bool bascule_tou_;
	
	float CONVERSION_TIC_MM_;
	float CONVERSION_TIC_RADIAN_;
	
	bool etat_rot_;
	bool etat_tra_;
	
	int32_t consigne_tra_;
	
	bool rotation_en_cours_;
	
	bool translation_attendue_;
	bool rotation_attendue_;
	bool goto_attendu_;
	
	int32_t mesure_distance_;
	int32_t mesure_angle_;
	
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
	
	//gestion des mesures courantes
	void mesure_angle(int32_t); 
	int32_t mesure_angle(void);
	void mesure_distance(int32_t); 
	int32_t mesure_distance(void);
	void envoyer_position_tic(void);
	
	void asservir();
	void update_position();
	void communiquer_pc();
	
	int32_t angle_initial(void);
	float angle_optimal(float angle, float angleBkp);
	
	int32_t angle_modulo_tic(int32_t angle);
	int32_t compare_angle_tic(int32_t angle1,int32_t angle2);
	
	void envoyer_acquittement(int16_t instruction = 0, char *new_message = NULL);
	void envoyer_position(void);
	
	void gotoPos(float x, float y);
	void debut_tourner(float angle);
	void fin_tourner(void);
	void debut_translater(float distance);
	void fin_translater(void);
	
	void debut_translater_seul(float distance);
	
	
	void stopper();
	void atteinte_consignes(void);
	void gestion_stoppage();
	
	void recalage(void);
	
	void translater_bloc(float distance);
	void tourner_bloc(float angle);
};

#endif
