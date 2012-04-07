#include <math.h>

#define PI 3.14159265
#define LARGEUR_ROBOT 200.0
#define LONGUEUR_TABLE 3000.0

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('v')
				,x_(0)
				,y_(0)
				,angle_serie_(0.0)
				,angle_origine_(0.0)
				,bascule_goto_(true)
				,bascule_tra_(true)
				,bascule_tou_(true)
				,rotation_en_cours_(false)
				,translation_attendue_(false)
				,rotation_attendue_(false)
				,goto_attendu_(false)
				,etat_rot_(true)
				,etat_tra_(true)
				,translation(0.6,2.5,0.0)//(1.4,6.0,0.0)
				,rotation(1.0,3.0,0.0)//(1.3,6.0,0.0)//(1.5,6.5,0.0)
				,CONVERSION_TIC_MM_(0.10360)//0.1061)
				,CONVERSION_TIC_RADIAN_(0.000703762)//0.000705976)//0.00070226)//0.000703)//0.000737463064)
				
{
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);
	
	changer_orientation(3.1415);
}

void Robot::asservir()
{
	int32_t pwmTranslation;
	int32_t pwmRotation;
	
	if (etat_rot_)
		pwmRotation = rotation.pwm(mesure_angle_,10);
	else
		pwmRotation = 0;
	
	if(etat_tra_)
		pwmTranslation = translation.pwm(mesure_distance_,20);
	else
		pwmTranslation = 0;
	
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
}


void Robot::update_position()
{
    
	static int32_t last_distance = 0;
	static int32_t last_angle = 0;

	int16_t delta_distance_tic = mesure_distance_ - last_distance;
	int16_t delta_angle_tic = mesure_angle_ - last_angle;
	
	float last_angle_radian = last_angle* CONVERSION_TIC_RADIAN_;
	float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;
	
	x_ += ( delta_distance_mm * cos( last_angle_radian - angle_origine_ ) );
	y_ += ( delta_distance_mm * sin( last_angle_radian - angle_origine_) );
	
	angle_serie_ += delta_angle_tic * CONVERSION_TIC_RADIAN_;
	
	last_distance = mesure_distance_;
	last_angle = mesure_angle_;
	
}

////////////////////////////// PROTOCOLE SERIE ///////////////////////////////////
void Robot::communiquer_pc(){
	char buffer[17];
	uint8_t length = serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0

	if(COMPARE_BUFFER("?",1)){
		serial_t_::print(0);
	}

	else if(COMPARE_BUFFER("ccr",3)){
		couleur_ = 'r';
	}
	else if(COMPARE_BUFFER("ccv",3)){
		couleur_ = 'v';
	}
	
	else if(COMPARE_BUFFER("crp",3)){
		rotation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crd",3)){
		rotation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cri",3)){
		rotation.ki(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ctp",3)){
		translation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("ctd",3)){
		translation.kd(serial_t_::read_float());
}	
	else if(COMPARE_BUFFER("cti",3)){
		translation.ki(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("ctm",3)){
		translation.valeur_bridage(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crm",3)){
		rotation.valeur_bridage(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("cx",2)){
		x(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cy",2)){
		y(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("co",2)){
		changer_orientation(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("ec",2)){
		serial_t_::print((char)couleur_);
	}
	
	else if(COMPARE_BUFFER("erp",3)){
		serial_t_::print(rotation.kp());
	}
	else if(COMPARE_BUFFER("erd",3)){
		serial_t_::print(rotation.kd());
	}
	else if(COMPARE_BUFFER("eri",3)){
		serial_t_::print(rotation.ki());
	}
	else if(COMPARE_BUFFER("erm",3)){
		serial_t_::print(rotation.valeur_bridage());
	}

	else if(COMPARE_BUFFER("etp",3)){
		serial_t_::print(translation.kp());
	}
	else if(COMPARE_BUFFER("etd",3)){
		serial_t_::print(translation.kd());
	}
	else if(COMPARE_BUFFER("eti",3)){
		serial_t_::print(translation.ki());
	}
	else if(COMPARE_BUFFER("etm",3)){
		serial_t_::print(translation.valeur_bridage());
	}
	
	else if(COMPARE_BUFFER("ex",2)){
		serial_t_::print((int32_t)x());
	}
	else if(COMPARE_BUFFER("ey",2)){
		serial_t_::print((int32_t)y());
	}
	else if(COMPARE_BUFFER("eo",2)){
		serial_t_::print((int32_t)((float)angle_serie_ * 1000));
	}
	
	else if(COMPARE_BUFFER("d",1)){
		
		envoyer_acquittement(-1);
		
		debut_translater_seul(serial_t_::read_float());
		
		/*
		debut_translater(serial_t_::read_float());
		rotation_en_cours_ = true;
		*/
		
		/*
		float dist = serial_t_::read_float();
		goto_attendu_ = true;
		debut_translater(dist);
		debut_tourner(angle_serie_);
		*/
	}
	else if(COMPARE_BUFFER("t",1)){
		envoyer_acquittement(-1);
		debut_tourner(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("goto",4)){
		envoyer_acquittement(-1);
		
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();      
		gotoPos(co_x , co_y);
	}
	
	else if(COMPARE_BUFFER("stop",4)){
		stopper();
	}
	
	//stopper asservissement rotation/translation
	else if(COMPARE_BUFFER("cr0",3)){
		etat_rot_ = false;
	}
	else if(COMPARE_BUFFER("ct0",3)){
		etat_tra_ = false;
	}
	
	//démarrer asservissement rotation/translation
	else if(COMPARE_BUFFER("cr1",3)){
		etat_rot_ = true;
	}
	else if(COMPARE_BUFFER("ct1",3)){
		etat_tra_ = true;
	}
	
	//recalage de la position
	else if(COMPARE_BUFFER("recal",5)){
		recalage();
	}
	//arrete l'envoi d'acquittement en boucle (protocole explicite...)
	else if(COMPARE_BUFFER("TG",2)){
		envoyer_acquittement(-1);
	}
	//demande d'acquittement
	else if (COMPARE_BUFFER("acq",3)){
		envoyer_acquittement();
	}
	else if (COMPARE_BUFFER("ok",2)){
		envoyer_acquittement();
	}
	//demande de la position courante
	else if (COMPARE_BUFFER("pos",3)){
		envoyer_position();
	}
	else if (COMPARE_BUFFER("kadoc",5)){
	
	Serial<0>::print("////");
	serial_t_::print((int32_t)mesure_distance_);
	serial_t_::print((int32_t)(angle_origine_/CONVERSION_TIC_RADIAN_));
	serial_t_::print((int32_t)rotation.consigne());
	}
	

#undef COMPARE_BUFFER
}


////////////////////////////// ACCESSEURS /////////////////////////////////

unsigned char Robot::couleur(void)
{
return couleur_;
}

void Robot::couleur(unsigned char couleur)
{ 
	if (couleur == 'r' || couleur == 'v')
		couleur_ = couleur;
}

float Robot::x(void)
{
return (float)x_;
}

void Robot::x(float new_x)
{
	x_ = new_x;
}

float Robot::y(void)
{
return (float)y_;
}

void Robot::y(float new_y)
{
	y_ = new_y;
}

int32_t Robot::mesure_angle(void)
{
return (int32_t)mesure_angle_;
}
void Robot::mesure_angle(int32_t new_angle)
{
	mesure_angle_ = new_angle;
}

int32_t Robot::mesure_distance(void)
{
return (int32_t)mesure_distance_;
}
void Robot::mesure_distance(int32_t new_distance)
{
	mesure_distance_ = new_distance;
}

////////////////////////////// CALCULS ET ENVOIS SUR SERIE ////////////////////////////////


int32_t Robot::angle_initial()
{
	if (couleur_ == 'r')
		return 0;
	else
		return 4260;
}

float Robot::angle_optimal(float angle, float angleBkp)
{
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
	return angle;
}

int32_t Robot::angle_modulo_tic(int32_t angle)
{
	while (angle < 0)
		angle += 8928;//2*pi
	while (angle >= 8928)
		angle -= 8928;//2*pi
	return angle;
}

void Robot::changer_orientation(float new_angle)
{
	float new_angle_rad = angle_optimal(new_angle, mesure_angle_*CONVERSION_TIC_RADIAN_);
	int32_t new_angle_tic = new_angle_rad/CONVERSION_TIC_RADIAN_;
	
	mesure_angle_ = new_angle_tic;
	angle_origine_ += new_angle_rad - angle_serie_;
	angle_serie_ = new_angle_rad;
}

void Robot::envoyer_acquittement(int16_t instruction, char *new_message)
{
	/*
	 * les entiers envoi et instruction permettent d'accelerer la gestion de la nouvelle entrée string :
	
	 * l'entier envoi sauvegarde le type du dernier message envoyé :
	 * 0 indique que le message ne sera pas envoyé
	 * 1 indique qu'un message d'acquittement "FIN_..." est stocké dans message
	 * 2 indique qu'un message d'acquittement goto "FIN_GOTO" est stocké dans message
	 * 3 indique qu'un message d'arret "STOPPE" est stocké dans message
	 
	 * l'entier instruction modifie les variables statiques :
	 * 1 indique qu'un nouveau message d'acquittement doit etre envoyé
	 * 2 indique qu'un nouveau message d'acquittement goto doit etre envoyé
	 * 3 indique qu'un nouveau message d'arrêt doit etre envoyé
	 * 0 ne modifie pas le message envoyé (l'appel envoie juste l'ancien message sur la série)
	 * -1 arrete l'envoi sur la série
	*/
	
	static char *message = "";
	static int16_t envoi = 0;
	
	if (instruction)
	{
		if (instruction == -1)
		{
			envoi = 0;
		}
		else if (instruction == 1 && envoi < 2)
		{
			envoi = 1;
			message = new_message;
		}
		else if (instruction == 2 && envoi < 3)
		{
			envoi = 2;
			message = new_message;
		}
		else if (instruction == 3)
		{
			envoi = 3;
			message = new_message;
		}
	}
	if (envoi && not instruction)
		Serial<0>::print(message);
	
}
	
void Robot::envoyer_position()
{
	serial_t_::print((int32_t)x(),(int32_t)y());
// 	serial_t_::print((int32_t)((float)angle_serie_ * 1000));
}

void Robot::envoyer_position_tic()
{
// 	serial_t_::print((int32_t)mesure_distance_);
	serial_t_::print((int32_t)mesure_angle_);
}


////////////////////////////// DEPLACEMENTS ET STOPPAGE ///////////////////////////////////


void Robot::gotoPos(float x, float y)
{
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle = atan2(delta_y,delta_x);
	goto_attendu_ = true;
	debut_tourner(angle);
	debut_translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}

void Robot::debut_tourner(float angle)
{
	envoyer_acquittement(-1);
	float new_angle = angle_optimal(angle - angle_origine_, mesure_angle_*CONVERSION_TIC_RADIAN_);
	
	rotation_attendue_ = true;
	rotation.consigne(new_angle/CONVERSION_TIC_RADIAN_);
	envoyer_acquittement(1,"EN_MVT");
}
	
	
void Robot::fin_tourner()
{
	/*
	if (consigne_tra_ != translation.consigne())
	{
		translation.consigne(consigne_tra_);
		translation_attendue_ = true;
	}*/
	
	//@@@@
	if (rotation_attendue_ && abs( angle_modulo_tic(mesure_distance_+ angle_origine_/CONVERSION_TIC_RADIAN_) - angle_modulo_tic(rotation.consigne()) ) < 1000)//250 tic : 10 degrés)
	{
		rotation_attendue_ = false;
		if (goto_attendu_)
		{
			translation_attendue_ = true;
			translation.consigne(consigne_tra_);
		}
		else
		{
			/*
			if (bascule_tou_)
				envoyer_acquittement(1,"FIN_TOUA");
			else
				envoyer_acquittement(1,"FIN_TOUB");
			bascule_tou_ = !bascule_tou_;
			*/
			envoyer_acquittement(2,"FIN_MVT");
		}
	}
}

void Robot::debut_translater_seul(float distance)
{
	translation_attendue_ = true;
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
	translation.consigne(translation.consigne()+distance/CONVERSION_TIC_MM_);
	envoyer_acquittement(1,"EN_MVT");
}

void Robot::debut_translater(float distance)
{	
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
}


void Robot::fin_translater()
{
	if (translation_attendue_)
	{
		translation_attendue_ = false;

		if (goto_attendu_)
			goto_attendu_ = false;
		envoyer_acquittement(2,"FIN_MVT");
		/*
		if (goto_attendu_)
		{
			goto_attendu_ = false;
			if (bascule_goto_)
				envoyer_acquittement(2,"FIN_GOTOA");
			else
				envoyer_acquittement(2,"FIN_GOTOB");
			bascule_goto_ = !bascule_goto_;
		}
		else
		{
			if (bascule_tra_)
				envoyer_acquittement(1,"FIN_TRAA");
			else
				envoyer_acquittement(1,"FIN_TRAB");
			bascule_tra_ = !bascule_tra_;
			
		}
		*/
		
	}
}

void Robot::stopper()
{
	/*
	//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
	rotation.consigne(mesure_angle_);
	//stop en translation
	consigne_tra_ = mesure_distance_;
	translation.consigne(mesure_distance_);
 	if (goto_attendu_ || translation_attendue_ || rotation_attendue_)
		envoyer_acquittement(3,"STOPPE");
	*/
	
	if (goto_attendu_ || translation_attendue_ || rotation_attendue_)
	{
		if (rotation_attendue_ && abs(mesure_angle_ - rotation.consigne())<25)
			fin_tourner();
		else if (translation_attendue_ && abs(mesure_distance_ - translation.consigne())<50)
			fin_translater();
		else 
		{
			envoyer_acquittement(3,"STOPPE");
			//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
			rotation.consigne(mesure_angle_);
			//stop en translation
			consigne_tra_ = mesure_distance_;
			translation.consigne(mesure_distance_);
		}
	}
	else
	{
		//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
		rotation.consigne(mesure_angle_);
		//stop en translation
		consigne_tra_ = mesure_distance_;
		translation.consigne(mesure_distance_);
	}
}

void Robot::atteinte_consignes()
{
	static bool translation_en_cours = false;
	
	if (abs(rotation.pwmCourant())>=10)
		rotation_en_cours_ = true;

	if (rotation_en_cours_ && abs(rotation.pwmCourant())<10)
	{
		rotation_en_cours_ = false;
		fin_tourner();
	}
	
	if (abs(translation.pwmCourant())>=10)
		translation_en_cours = true;

	if (translation_en_cours && abs(translation.pwmCourant())<10 && abs(mesure_distance_ - translation.consigne())<300)//3 cm
	{
		translation_en_cours = false;
		fin_translater();
	}
}

void Robot::gestion_stoppage()
{
	
	static float compteurBlocage=0;
	static int32_t T_last_distance[] = {2147423647,2147483647,2147483647,2147483647,2147483647};
	static int32_t T_last_angle[] = {2147423647,2147483647,2147483647,2147483647,2147483647};
	
	/*
	static int32_t last_distance;
	static int32_t last_angle;
	*/
	
	//detection d'un blocage - translation
	if (	   (abs(rotation.pwmCourant())>0
		&& abs(T_last_angle[4]-T_last_angle[0])<5)
		|| (abs(translation.pwmCourant())>0
		&& abs(T_last_distance[4]-T_last_distance[0])<5)
	   )
	{
			
		if(compteurBlocage==20){
			stopper();
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
	
	for (int16_t i=4;i>0;i--)
		T_last_distance[i] = T_last_distance[i-1];
	T_last_distance[0] = mesure_distance_;
	
	/*
	last_distance = mesure_distance_;
	last_angle = mesure_angle_;
	*/
}

/////////////////////////// FONCTIONS BLOQUANTES POUR LE RECALAGE ///////////////////////

void Robot::recalage()
{
	
	translation.valeur_bridage(50.0);
	rotation.valeur_bridage(100.0);
	translater_bloc(-300.0);
	etat_rot_ = false;
	translater_bloc(-200.0);
	if (couleur_ == 'r') x(-LONGUEUR_TABLE/2+LARGEUR_ROBOT/2); else x(LONGUEUR_TABLE/2-LARGEUR_ROBOT/2);
	if (couleur_ == 'r') changer_orientation(0.0); else changer_orientation(PI);
	etat_rot_ = true;
	translater_bloc(300.0);
	tourner_bloc(PI/2);
	translater_bloc(-300.0);
	etat_rot_ = false;
	translater_bloc(-300.0);
	y(LARGEUR_ROBOT/2);
	changer_orientation(PI/2);
	etat_rot_ = true;
	translater_bloc(150.0);
	rotation.valeur_bridage(250.0);
	if (couleur_ == 'r') tourner_bloc(0.0); else tourner_bloc(PI);
	translation.valeur_bridage(250.0);
	envoyer_acquittement(2,"FIN_REC");
	etat_rot_ = false;
	etat_tra_ = false;
	
}

void Robot::translater_bloc(float distance)
{	
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
	translation.consigne(consigne_tra_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(translation.pwmCourant())> 10){
		asm("nop");
	}
}

void Robot::tourner_bloc(float angle)
{
	float new_angle = angle_optimal(angle - angle_origine_, mesure_angle_*CONVERSION_TIC_RADIAN_);
	rotation.consigne(new_angle/CONVERSION_TIC_RADIAN_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(rotation.pwmCourant())> 10){
		asm("nop");
	}
}