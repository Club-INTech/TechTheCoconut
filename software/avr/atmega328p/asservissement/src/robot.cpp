#include <math.h>
#define PI 3.14159265

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
				,last_tic_rot_(0)
				,last_tic_tra_(0)
				,angle_courant_(0.0)
				,translation_en_cours_(false)
				,rotation_en_cours_(false)
				,translation_attendue_(false)
				,rotation_attendue_(false)
				,goto_attendu_(false)
				,etat_rot_(true)
				,etat_tra_(true)
				,demande_stop_(false)
				,translation(0.6,2,0.0)
				,rotation(1,3,0.0)
// 				,translation(0.6,3,0.01)
// 				,rotation(0.4,3,0.01)
				,CONVERSION_TIC_MM_(0.1061)
				,CONVERSION_TIC_RADIAN_(0.000737463064)
	
	
{
	
	
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);
	
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int32_t pwmTranslation = translation.pwm(distance);
	int32_t pwmRotation = rotation.pwm(angle);
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
}



void Robot::updatePosition(int32_t distance, int32_t angle)
{
    
	static int32_t last_distance = 0;
	static int32_t last_angle = 0;

	int16_t delta_distance_tic = distance - last_distance;
	int16_t delta_angle_tic = angle - last_angle;
	int32_t last_angle_abs;
    
	if(couleur_ == 'v')
	{
		last_angle_abs= (last_angle + 4260);
	}else{
		last_angle_abs = last_angle;
	}
		
	float last_angle_radian = last_angle_abs* CONVERSION_TIC_RADIAN_;
	float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;
	x_ += ( delta_distance_mm * cos( last_angle_radian ) );
	y_ += ( delta_distance_mm * sin( last_angle_radian ) );
	
	
	
	angle_courant((float) angle_courant() + delta_angle_tic * CONVERSION_TIC_RADIAN_);
	
	last_distance = distance;
	
	last_angle = angle;
	
}

//TODO Finir implémentation de protocole.txt
void Robot::communiquer_pc(){
	char buffer[17];
	uint8_t length = serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string) strncmp(buffer, string, length) == 0 && length>0

	if(COMPARE_BUFFER("?")){
		serial_t_::print(0);
	}

	else if(COMPARE_BUFFER("ccr")){
		couleur_ = 'r';
	}
	else if(COMPARE_BUFFER("ccv")){
		couleur_ = 'v';
	}
	
	else if(COMPARE_BUFFER("crp")){
		rotation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crd")){
		rotation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cri")){
		rotation.ki(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ctp")){
		translation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("ctd")){
		translation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cti")){
		translation.ki(serial_t_::read_float());
	}
	//TODO ctm crm :  Max du PWM
	
	else if(COMPARE_BUFFER("cx")){
		x(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cy")){
		y(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ec")){
		serial_t_::print((char)couleur_);
	}
	
	else if(COMPARE_BUFFER("erp")){
		serial_t_::print(rotation.kp());
	}
	else if(COMPARE_BUFFER("erd")){
		serial_t_::print(rotation.kd());
	}
	else if(COMPARE_BUFFER("eri")){
		serial_t_::print(rotation.ki());
	}
	else if(COMPARE_BUFFER("erm")){
		serial_t_::print(rotation.valeur_bridage());
	}

	else if(COMPARE_BUFFER("etp")){
		serial_t_::print(translation.kp());
	}
	else if(COMPARE_BUFFER("etd")){
		serial_t_::print(translation.kd());
	}
	else if(COMPARE_BUFFER("eti")){
		serial_t_::print(translation.ki());
	}
	else if(COMPARE_BUFFER("etm")){
		serial_t_::print(translation.valeur_bridage());
	}
	
	else if(COMPARE_BUFFER("ex")){
		serial_t_::print((int32_t)x());
	}
	else if(COMPARE_BUFFER("ey")){
		serial_t_::print((int32_t)y());
	}
	else if(COMPARE_BUFFER("eo")){
		serial_t_::print((int32_t)angle_courant()*1000);
	}
	
	else if(COMPARE_BUFFER("d")){
// 		translater(serial_t_::read_float());
		debut_translater(serial_t_::read_float());
		rotation_en_cours(true);
	}
	else if(COMPARE_BUFFER("t")){
// 		tourner(serial_t_::read_float());
		debut_tourner(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("goto")){
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();
		gotoPos(co_x , co_y);
	}
	
	else if(COMPARE_BUFFER("stop")){
		demande_stop(true);
	}
	
	//stopper asservissement rotation/translation
	else if(COMPARE_BUFFER("sr")){
		etat_rot(false);
	}
	else if(COMPARE_BUFFER("st")){
		etat_tra(false);
	}
	
	//démarrer asservissement rotation/translation
	else if(COMPARE_BUFFER("dr")){
		etat_rot(true);
	}
	else if(COMPARE_BUFFER("dt")){
		etat_tra(true);
	}

#undef COMPARE_BUFFER
}

void Robot::couleur(unsigned char couleur)
{ 
	if (couleur == 'r' || couleur == 'v')
		couleur_ = couleur;
}

unsigned char Robot::couleur(void)
{
return couleur_;
}

float Robot::x(void)
{
return (float)x_;
}

float Robot::y(void)
{
return (float)y_;
}

float Robot::angle_courant(void)
{
return (float)angle_courant_;
}

bool Robot::etat_rot(void)
{
return (bool)etat_rot_;
}
bool Robot::etat_tra(void)
{
return (bool)etat_tra_;
}

int32_t Robot::consigne_tra(void)
{
return (int32_t)consigne_tra_;

}
int32_t Robot::consigne_rot(void)
{
return (int32_t)consigne_rot_;
}


int32_t Robot::tra_pwmCourant(void)
{
return (int32_t)translation.pwmCourant();
}
int32_t Robot::rot_pwmCourant(void)
{
return (int32_t)rotation.pwmCourant();
}

int32_t Robot::tra_consigne(void)
{
return (int32_t)translation.consigne();
}
int32_t Robot::rot_consigne(void)
{
return (int32_t)rotation.consigne();
}

bool Robot::translation_en_cours(void)
{
return (bool)translation_en_cours_;
}

bool Robot::rotation_en_cours(void)
{
return (bool)rotation_en_cours_;
}

void Robot::translation_en_cours(bool etat)
{
	translation_en_cours_ = etat;
}
void Robot::rotation_en_cours(bool etat)
{
	rotation_en_cours_ = etat;
}



bool Robot::translation_attendue(void)
{
return (bool)translation_attendue_;
}

bool Robot::rotation_attendue(void)
{
return (bool)rotation_attendue_;
}

void Robot::translation_attendue(bool etat)
{
	translation_attendue_ = etat;
}
void Robot::rotation_attendue(bool etat)
{
	rotation_attendue_ = etat;
}

bool Robot::goto_attendu(void)
{
return (bool)goto_attendu_;
}

void Robot::goto_attendu(bool etat)
{
	goto_attendu_ = etat;
}


bool Robot::demande_stop(void)
{
return (bool)demande_stop_;
}

void Robot::demande_stop(bool etat)
{
	demande_stop_ = etat;
}

int32_t Robot::last_tic_tra(void)
{
return (int32_t)last_tic_tra_;
}

void Robot::last_tic_tra(int32_t valeur)
{
	last_tic_tra_ = valeur;
}

int32_t Robot::last_tic_rot(void)
{
return (int32_t)last_tic_rot_;
}

void Robot::last_tic_rot(int32_t valeur)
{
	last_tic_rot_ = valeur;
}

void Robot::x(float new_x)
{
	x_ = new_x;
}

void Robot::y(float new_y)
{
	y_ = new_y;
}

void Robot::angle_courant(float new_angle)
{
	angle_courant_ = new_angle;
}


void Robot::etat_rot(bool etat)
{
	etat_rot_ = etat;
}
void Robot::etat_tra(bool etat)
{
	etat_tra_ = etat;
}

void Robot::consigne_tra(int32_t cons)
{
	consigne_tra_ = cons;
}
void Robot::consigne_rot(int32_t cons)
{
	consigne_rot_ = cons;
}


	

void Robot::gotoPos(float x, float y)
{
	
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle;
	
	angle=atan2(delta_y,delta_x);
	
	goto_attendu(true);
	
	debut_tourner(angle);
	
	debut_translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}

/*
/////////  méthodes  bloquantes ///////////

void Robot::translater(float distance)
{	
	
	translation.consigne(translation.consigne()+distance/CONVERSION_TIC_MM_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(translation.pwmCourant())> 10){
		asm("nop");
	}
}

void Robot::tourner(float angle)
{
	
// 	serial_t_::print(rotation.consigne()*CONVERSION_TIC_RADIAN_*1000);
// 	serial_t_::print(angle*1000);
	
	static float angleBkp = 0;
	//angledepart_? (couleur_ == 'v') PI : 
	
	
	float ang1 = abs(angle-angleBkp);
	float ang2 = abs(angle+2*PI-angleBkp);
	float ang3 = abs(angle-2*PI-angleBkp);
	
	if (!(ang1 < ang2 && ang1 < ang3))
	{
		if (ang2 < ang3)
			angle += 2*PI;
		else
			angle -=  2*PI;
	}
	angleBkp=angle;
	
	
	rotation.consigne(angle/CONVERSION_TIC_RADIAN_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(rotation.pwmCourant())> 10){
		asm("nop");
	}	
}
*/


void Robot::debut_tourner(float angle)
{
	static float angleBkp = 0;
	//angledepart_? (couleur_ == 'v') PI : 
	
	rotation_attendue(true);
	
	float ang1 = abs(angle-angleBkp);
	float ang2 = abs(angle+2*PI-angleBkp);
	float ang3 = abs(angle-2*PI-angleBkp);
	
	if (!(ang1 < ang2 && ang1 < ang3))
	{
		if (ang2 < ang3)
			angle += 2*PI;
		else
			angle -=  2*PI;
	}
	angleBkp=angle;
	
	
	rotation.consigne(angle/CONVERSION_TIC_RADIAN_);
}
	
	
	
void Robot::fin_tourner()
{
	
	if (consigne_tra() != translation.consigne())
	{
		translation.consigne(consigne_tra());
	}
	//else if (abs(angle_courant_ == rotation.consigne()*CONVERSION_TIC_RADIAN_) < 0.01)
	else if (rotation_attendue())
	{
		rotation_attendue(false);
		if (not goto_attendu())
		{
			//fin d'un ordre de rotation simple
			Serial<0>::print("FIN_TOU");
		}else{
			//fin d'un ordre de goto
			goto_attendu(false);
			Serial<0>::print("FIN_GOTO");
		}
	}
}

void Robot::debut_translater(float distance)
{	
	translation_attendue(true);
	consigne_tra(translation.consigne()+distance/CONVERSION_TIC_MM_);
}


void Robot::fin_translater()
{
	if (translation_attendue())
	{
		translation_attendue(false);
		if (not goto_attendu())
			Serial<0>::print("FIN_TRA");
	}
}

void Robot::stopper(int32_t distance)
{
	demande_stop(false);
	
	//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
	consigne_rot(angle_courant()/CONVERSION_TIC_RADIAN_);
	rotation.consigne(consigne_rot());
	//stop en translation
	consigne_tra(distance);
	translation.consigne(distance);
}

void Robot::trace(int32_t debug)
{
	serial_t_::print((int32_t)debug);
}


void Robot::atteinteConsignes()
{
	if (abs(rot_pwmCourant())>=10)
		rotation_en_cours(true);

	if (rotation_en_cours() && abs(rot_pwmCourant())<10)
	{
		
		rotation_en_cours(false);
		fin_tourner();
	}
	
	if (abs(tra_pwmCourant())>=10)
		translation_en_cours(true);

	if (translation_en_cours() && abs(tra_pwmCourant())<10)
	{
		translation_en_cours(false);
		fin_translater();
	}
}

void Robot::gestionStoppage(int32_t distance, int32_t angle)
{
	
	static float compteurBlocage=0;
	static int32_t last_distance;
	static int32_t last_angle;
	
	
	//gestion de l'arret
	if (demande_stop())
		stopper(distance);
	
	
	
	//detection d'un blocage - translation
		
	//2500 ne stoppe pas | 2000 ne démarre pas | 2200 ne stop pas ET ne démarre pas...
// 	if(abs(robot.tra_pwmCourant())>2150 && abs(distance-robot.last_tic_tra())==0)
		
		
	if (	   abs(rot_pwmCourant())>0 
		&& abs(tra_pwmCourant())>0 
		&& abs(last_distance-distance)<10
		&& abs(last_angle-angle)<10
	   )
	{
			
		if(compteurBlocage==20){
			demande_stop(true);
			compteurBlocage=0;
		}
		else{
			compteurBlocage++;
		}
		
	}
	else
	{
		compteurBlocage=0;
	}
	
	
	last_distance = distance;
	last_angle = angle;
		
	/*	
	if(abs(tra_consigne()-distance) > (abs(tra_consigne()-last_tic_tra()) - 20))
	{
// 		robot.trace(abs(distance-robot.last_tic_tra()));
		demande_stop(true);
	}*/
	
	/*
	//detection d'un blocage - rotation
	if(abs(robot.rot_pwmCourant())>200 && abs(infos[1]-robot.last_tic_rot())<50)
		robot.demande_stop(true);
	
	*/
	
}