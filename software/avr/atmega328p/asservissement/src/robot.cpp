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
				,rotation_en_cours_(false)
				,translation_attendue_(false)
				,rotation_attendue_(false)
				,goto_attendu_(false)
				,etat_rot_(true)
				,etat_tra_(true)
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

void Robot::asservir()
{
	int32_t pwmTranslation;
	int32_t pwmRotation;
	
	if (etat_rot_)
		pwmRotation = rotation.pwm(mesure_angle_);
	else
		pwmRotation = 0;
	
	if(etat_tra_)
		pwmTranslation = translation.pwm(mesure_distance_);
	else
		pwmTranslation = 0;
	
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
}



void Robot::updatePosition()
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
	else if(COMPARE_BUFFER("ctm")){
		translation.valeur_bridage(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crm")){
		rotation.valeur_bridage(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("cx")){
		x(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cy")){
		y(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("co")){
		changer_orientation(serial_t_::read_float());
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
		serial_t_::print((int32_t)((float)angle_serie_ * 1000));
	}
	
	else if(COMPARE_BUFFER("d")){
		envoyer_acquittement(-1);
		
		debut_translater(serial_t_::read_float());
		rotation_en_cours_ = true;
	}
	else if(COMPARE_BUFFER("t")){
		envoyer_acquittement(-1);
		
		debut_tourner(serial_t_::read_float());
	}
	
	else if(COMPARE_BUFFER("goto")){
		envoyer_acquittement(-1);
		
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();      
		gotoPos(co_x , co_y);
	}
	
	else if(COMPARE_BUFFER("stop")){
		stopper();
	}
	
	//stopper asservissement rotation/translation
	else if(COMPARE_BUFFER("cr0")){
		etat_rot_ = false;
	}
	else if(COMPARE_BUFFER("ct0")){
		etat_tra_ = false;
	}
	
	//démarrer asservissement rotation/translation
	else if(COMPARE_BUFFER("cr1")){
		etat_rot_ = true;
	}
	else if(COMPARE_BUFFER("ct1")){
		etat_tra_ = true;
	}
	
	//recalage de la position
	else if(COMPARE_BUFFER("recal")){
		recalage();
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

////////////////////////////// DEPLACEMENTS ET STOPPAGE ///////////////////////////////////


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
	 * 2 indique qu'un message d'arret "STOPPE" est stocké dans message
	 
	 * l'entier instruction modifie les variables statiques :
	 * 1 indique qu'un nouveau message d'acquittement doit etre envoyé
	 * 2 indique qu'un nouveau message d'arrêt doit etre envoyé
	 * 0 ne modifie pas le message envoyé (l'appel envoie juste l'ancien message sur la série)
	 * -1 arrete l'envoi sur la série
	*/
	
	static char *message = "";
	static int16_t envoi = 0;
	
	if (instruction)
	{
		if (instruction == -1)
			envoi = 0;
		else if (instruction == 1 && envoi < 2)
		{
			envoi = 1;
			message = new_message;
		}
		else if (instruction == 2)
		{
			envoi = 2;
			message = new_message;
		}
	}
	if (envoi)
		Serial<0>::print(message);
}

void Robot::envoyer_position()
{
	serial_t_::print((int32_t)(x()*100000 + y()));
}

void Robot::gotoPos(float x, float y)
{
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle;
	angle=atan2(delta_y,delta_x);
	goto_attendu_ = true;
	debut_tourner(angle);
	debut_translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}

void Robot::debut_tourner(float angle)
{
	float new_angle = angle_optimal(angle - angle_origine_, mesure_angle_*CONVERSION_TIC_RADIAN_);
	
	rotation_attendue_ = true;
	rotation.consigne(new_angle/CONVERSION_TIC_RADIAN_);
}
	
	
	
void Robot::fin_tourner()
{
	if (consigne_tra_ != translation.consigne())
	{
		translation.consigne(consigne_tra_);
		translation_attendue_ = true;
	}
	else if (rotation_attendue_)
	{
		rotation_attendue_ = false;
		if (not goto_attendu_)
			envoyer_acquittement(1,"FIN_TOU");
	}
}

void Robot::debut_translater(float distance)
{	
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
}


void Robot::fin_translater()
{
	if (translation_attendue_ && abs(mesure_distance_ - translation.consigne())<100)
	{
		translation_attendue_ = false;
		if (goto_attendu_)
		{
			goto_attendu_ = false;
			envoyer_acquittement(1,"FIN_GOTO");
		}
		else
			envoyer_acquittement(1,"FIN_TRA");
	}
}

void Robot::stopper()
{
	//stop en rotation. risque de tour sur lui meme ? (probleme +/- 2pi)
	rotation.consigne(mesure_angle_);
	//stop en translation
	consigne_tra_ = mesure_distance_;
	translation.consigne(mesure_distance_);
	if (goto_attendu_ || translation_attendue_ || rotation_attendue_)
		envoyer_acquittement(2,"STOPPE");
}

void Robot::atteinteConsignes()
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

	if (translation_en_cours && abs(translation.pwmCourant())<10)
	{
		translation_en_cours = false;
		fin_translater();
	}
}

void Robot::gestionStoppage()
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
		&& abs(T_last_angle[4]-T_last_angle[0])<10)
		|| (abs(translation.pwmCourant())>0
		&& abs(T_last_distance[4]-T_last_distance[0])<10)
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

void Robot::recalage()
{
	
	translation.valeur_bridage(50.0);
	translater(-300.0);
	etat_rot_ = false;
	translater(-200.0);
	if (couleur_ == 'r') x(-LONGUEUR_TABLE/2+LARGEUR_ROBOT/2); else x(LONGUEUR_TABLE/2-LARGEUR_ROBOT/2);
	if (couleur_ == 'r') changer_orientation(0.0); else changer_orientation(PI);
	etat_rot_ = true;
	translater(300.0);
	tourner(PI/2);
	translater(-300.0);
	etat_rot_ = false;
	translater(-200.0);
	y(LARGEUR_ROBOT/2);
	changer_orientation(PI/2);
	etat_rot_ = true;
	translater(150.0);
	if (couleur_ == 'r') tourner(0.0); else tourner(PI);
	etat_rot_ = false;
	etat_tra_ = false;
	envoyer_acquittement(1,"FIN_REC");
	translation.valeur_bridage(255.0);
	
}

void Robot::translater(float distance)
{	
	consigne_tra_ = translation.consigne()+distance/CONVERSION_TIC_MM_;
	translation.consigne(consigne_tra_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(translation.pwmCourant())> 10){
		asm("nop");
	}
}

void Robot::tourner(float angle)
{
	float new_angle = angle_optimal(angle - angle_origine_, mesure_angle_*CONVERSION_TIC_RADIAN_);
	rotation.consigne(new_angle/CONVERSION_TIC_RADIAN_);
	while(compteur.value()>0){ asm("nop"); }
	while(abs(rotation.pwmCourant())> 10){
		asm("nop");
	}
}