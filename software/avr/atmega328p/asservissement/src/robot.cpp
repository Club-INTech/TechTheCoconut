#include <math.h>

#define PI 3.14159265
#define LARGEUR_ROBOT 200.0
#define LONGUEUR_TABLE 3000.0
#define PI_TIC 4414
#define PI_fois2_TIC 8828

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>

#include <util/delay.h>


// Constructeur avec assignation des attributs
Robot::Robot() : 		couleur_('v')
				,x_(0)
				,y_(0)
				,angle_serie_(0.0)
				,angle_origine_(0.0)
				,etat_rot_(true)
				,etat_tra_(true)
				,est_bloque_(false)
				,translation(0.75,3.5,0.0)//(0.6,2.5,0.0)//(1.4,6.0,0.0)
				,rotation(0.9,3.5,0.0)//(1.3,6.0,0.0)//(1.5,6.5,0.0)
				,CONVERSION_TIC_MM_(0.10360)//0.1061)
				,CONVERSION_TIC_RADIAN_(0.0007117)//0.000705976)//0.00070226)//0.000703)//0.000737463064)

{
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);

	changer_orientation(3.1415);

	translation.valeur_bridage(100.0);
	translation.kp(0.75);
	translation.kd(2.5);

	rotation.valeur_bridage(100.0);
	rotation.kp(1.2);
	rotation.kd(3.5);
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

	x_ += ( delta_distance_mm * cos(angle_serie_) );
	y_ += ( delta_distance_mm * sin(angle_serie_) );

	angle_serie_ += delta_angle_tic * CONVERSION_TIC_RADIAN_;

	last_distance = mesure_distance_;
	last_angle = mesure_angle_;

}

////////////////////////////// PROTOCOLE SERIE ///////////////////////////////////
void Robot::communiquer_pc(){
	char buffer[17];
	serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
	if(COMPARE_BUFFER("?",1)){
		serial_t_::print(0);
	}
	
	
	else if(COMPARE_BUFFER("eer",3)){
		serial_t_::print(abs(rotation.erreur()));
	}
	else if(COMPARE_BUFFER("eet",3)){
		serial_t_::print(abs(translation.consigne() - mesure_distance_));
	}
	
	else if(COMPARE_BUFFER("epr",3)){
		serial_t_::print(rotation.pwmCourant());
	}
	else if(COMPARE_BUFFER("ept",3)){
		serial_t_::print(translation.pwmCourant());
	}
	
	else if(COMPARE_BUFFER("epg",3)){
		serial_t_::print(moteurGauche.pwm());
	}
	else if(COMPARE_BUFFER("epd",3)){
		serial_t_::print(moteurDroit.pwm());
	}
	
	else if(COMPARE_BUFFER("cpg",3)){
		moteurGauche.envoyerPwm(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cpd",3)){
		moteurDroit.envoyerPwm(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cpr",3)){
		int16_t rotation = serial_t_::read_float();
		moteurGauche.envoyerPwm(- rotation);
		moteurDroit.envoyerPwm(rotation);
		
	}
	else if(COMPARE_BUFFER("cpt",3)){
		int16_t translation = serial_t_::read_float();
		moteurGauche.envoyerPwm(translation);
		moteurDroit.envoyerPwm(translation);
		
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
		translater(serial_t_::read_float());
	}

	else if(COMPARE_BUFFER("t",1)){
		tourner(serial_t_::read_float());
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

	//demande d'acquittement
	else if (COMPARE_BUFFER("acq",3))
	{
		if(est_stoppe())
		{
			if(est_bloque_)
				serial_t_::print("STOPPE");
			else
			{
				serial_t_::print("FIN_MVT");
			}
		}
		else
			serial_t_::print("EN_MVT");
// 		serial_t_::print(abs(rotation.erreur()));
// 		serial_t_::print(abs(translation.consigne() - mesure_distance_));
	}

	//demande de la position courante
	else if (COMPARE_BUFFER("pos",3)){
		envoyer_position();
	}

	////////////////////////////////////////vitesses prédéfinies
	else if (COMPARE_BUFFER("ctv1",4))
	{
		changerVitesseTra1();
	}
	else if (COMPARE_BUFFER("ctv2",4))
	{
		changerVitesseTra2();
	}
	else if (COMPARE_BUFFER("ctv3",4))
	{
		changerVitesseTra3();
	}
	else if (COMPARE_BUFFER("crv1",4))
	{
		changerVitesseRot1();
	}
	else if (COMPARE_BUFFER("crv2",4))
	{
		changerVitesseRot2();
	}
	else if (COMPARE_BUFFER("crv3",4))
	{
		changerVitesseRot3();
	}


#undef COMPARE_BUFFER
}
////////////////////////////// VITESSES /////////////////////////////

void Robot::changerVitesseTra1(void)
{
	translation.valeur_bridage(60.0);//50 avant balise, yeux, etc
	translation.kp(0.75);
	translation.kd(2.0);
}
void Robot::changerVitesseTra2(void)
{
	translation.valeur_bridage(100.0);
	translation.kp(0.75);
	translation.kd(2.5);

}
void Robot::changerVitesseTra3(void)
{
	translation.valeur_bridage(200.0);
	translation.kp(0.75);
	translation.kd(3.5);

}
void Robot::changerVitesseRot1(void)
{
	rotation.valeur_bridage(80.0);//70
	rotation.kp(1.5);
	rotation.kd(2.0);
}
void Robot::changerVitesseRot2(void)
{
	rotation.valeur_bridage(100.0);
	rotation.kp(1.2);
	rotation.kd(3.5);
}
void Robot::changerVitesseRot3(void)
{
	rotation.valeur_bridage(200.0);
	rotation.kp(0.9);
	rotation.kd(3.5);
}
////////////////////////////// ACCESSEURS /////////////////////////////////

unsigned char Robot::couleur(void)
{
	return couleur_;
}

void Robot::couleur(unsigned char couleur)
{
	couleur_ = couleur;
}

float Robot::x(void)
{
	return x_;
}

void Robot::x(float new_x)
{
	x_ = new_x;
}

float Robot::y(void)
{
	return y_;
}

void Robot::y(float new_y)
{
	y_ = new_y;
}

int32_t Robot::mesure_angle(void)
{
	return mesure_angle_;
}
void Robot::mesure_angle(int32_t new_angle)
{
	mesure_angle_ = new_angle;
}

int32_t Robot::mesure_distance(void)
{
	return mesure_distance_;
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
		return PI_TIC;
}

int32_t Robot::angle_optimal(int32_t angle, int32_t angleBkp)
{
	while (angle > angleBkp+PI_TIC)
		angle -= PI_fois2_TIC;
	while (angle <= angleBkp-PI_TIC)
		angle += PI_fois2_TIC;
	return angle;
}
/*
int32_t Robot::compare_angle_tic(int32_t angle1,int32_t angle2)
{
	//renvoit l'angle en tic minimisant le passage de angle1 à angle2
	while (angle1 < 0)
		angle1 += 8928;//2*pi
	while (angle2 < 0)
		angle2 += 8928;//2*pi

	int32_t diff = abs(angle1-angle2);
	while (diff >= 8928)
		diff -= 8928;
	if (diff > 4464)
		diff = 8928-diff;
	return diff;
}
*/
void Robot::changer_orientation(float new_angle)
{
	int32_t new_angle_tic = angle_optimal( new_angle/CONVERSION_TIC_RADIAN_, mesure_angle_ );
	float new_angle_rad = new_angle_tic*CONVERSION_TIC_RADIAN_;

	mesure_angle_ = new_angle_tic;
	angle_origine_ += new_angle_rad - angle_serie_;
	angle_serie_ = new_angle_rad;
}

void Robot::envoyer_position()
{
	//serial_t_::print((int32_t)x(),(int32_t)y());
	serial_t_::print((int32_t)x());
	serial_t_::print((int32_t)y());
}

void Robot::envoyer_position_tic()
{
	serial_t_::print((int32_t)mesure_distance_);
// 	serial_t_::print((int32_t)mesure_angle_);
}

bool Robot::est_stoppe()
{
	/*
	static bool mesure_ok = true;

	if ((abs(translation.consigne() - mesure_distance_) > 500 ||abs(compare_angle_tic(mesure_angle_,rotation.consigne())) > 1000) && mesure_ok)
	{
		mesure_ok = false;
		return false;
	}
	else
	{
		
		mesure_ok = true;
		*/
	
	//rotation : 17 en v1, 
//     serial_t_::print(abs(compare_angle_tic(mesure_angle_,rotation.consigne())));
//     serial_t_::print(abs(translation.consigne() - mesure_distance_));
	volatile bool rotation_stoppe = abs(rotation.erreur()) < 105;//37
	volatile bool translation_stoppe = abs(translation.erreur()) < 100;//42
	bool bouge_pas = rotation.erreur_d()==0 && translation.erreur_d()==0;
	return rotation_stoppe && translation_stoppe && bouge_pas;
	
// 	}
}


////////////////////////////// DEPLACEMENTS ET BLOCAGE ///////////////////////////////////

void Robot::tourner(float angle)
{
	est_bloque_ = false;
	float angle_tic = (angle - angle_origine_)/CONVERSION_TIC_RADIAN_;
	rotation.consigne(angle_optimal( angle_tic, mesure_angle_ ));
	while(compteur.value()>0){ asm("nop"); }

}

void Robot::translater(float distance)
{
	est_bloque_ = false;
	int32_t new_consigne = translation.consigne()+distance/CONVERSION_TIC_MM_;
	translation.consigne(new_consigne);
	while(compteur.value()>0){ asm("nop"); }
}

void Robot::stopper()
{
// 	serial_t_::print((int32_t)abs(compare_angle_tic(mesure_angle_,rotation.consigne())));
// 	serial_t_::print((int32_t)abs(translation.consigne() - mesure_distance_));
	if (not est_stoppe())
	{
	rotation.consigne(mesure_angle_);
	translation.consigne(mesure_distance_);
	}
}

void Robot::gestion_blocage()
{

	static float compteurBlocage=0;
// 	static int32_t T_last_distance[] = {2147423647,2147483647,2147483647,2147483647,2147483647};
// 	static int32_t T_last_angle[] = {2147423647,2147483647,2147483647,2147483647,2147483647};

	/*
	static int32_t last_distance;
	static int32_t last_angle;
	*/
	
	/*
	bool force_en_translation = (abs(rotation.pwmCourant())>40 && abs(T_last_angle[4]-T_last_angle[0])<5);
	bool force_en_rotation = (abs(translation.pwmCourant())>50 && abs(T_last_distance[4]-T_last_distance[0])<5);
	bool moteurs_forcent = force_en_translation || force_en_rotation;
	
	bool erreur_en_translation = abs(translation.consigne() - mesure_distance_) > 70;
	bool erreur_en_rotation = abs(compare_angle_tic(mesure_angle_,rotation.consigne())) > 65;
	
	bool important_ecart_en_translation = abs(mesure_distance_ - translation.consigne()) > 500;
	bool important_ecart_en_rotation = abs(compare_angle_tic(mesure_angle_,rotation.consigne())) > 500;
	bool on_peut_stopper_le_robot = (not est_bloque_) || ( est_bloque_ && (important_ecart_en_translation || important_ecart_en_rotation));
	*/
	
	bool moteur_force = abs(moteurGauche.pwm()) > 45 || abs(moteurDroit.pwm()) > 45;
	bool bouge_pas = rotation.erreur_d()==0 && translation.erreur_d()==0;
	
// 	serial_t_::print("###");
//     serial_t_::print(abs(moteurGauche.pwm()));
// 	serial_t_::print(abs(T_last_distance[4]-T_last_distance[0]));
// 	serial_t_::print(abs(T_last_angle[4]-T_last_angle[0]));
// 	serial_t_::print(moteurGauche.pwm());
// 	serial_t_::print(moteurDroit.pwm());
	
	if (bouge_pas && moteur_force)
	{
		if(compteurBlocage==20){
			stopper();
			est_bloque_ = true;
			compteurBlocage=0;
		}
		else
			compteurBlocage++;
	}
	else
	{
		compteurBlocage=0;
	}

// 	for (int16_t i=4;i>0;i--)
// 		T_last_distance[i] = T_last_distance[i-1];
// 	T_last_distance[0] = mesure_distance_;
// 	
// 	for (int16_t i=4;i>0;i--)
// 		T_last_angle[i] = T_last_angle[i-1];
// 	T_last_angle[0] = mesure_angle_;
	
	/*
	last_distance = mesure_distance_;
	last_angle = mesure_angle_;
	*/
}

/////////////////////////// FONCTIONS BLOQUANTES POUR LE RECALAGE ///////////////////////

void Robot::recalage()
{
	changerVitesseTra1();
	changerVitesseRot1();
	translater_bloc(-1000.0);
	etat_rot_ = false;
	changerVitesseTra2();
	translater_bloc(-300.0);
	if (couleur_ == 'r') x(-LONGUEUR_TABLE/2+LARGEUR_ROBOT/2); else x(LONGUEUR_TABLE/2-LARGEUR_ROBOT/2);
	if (couleur_ == 'r') changer_orientation(0.0); else changer_orientation(PI);
	etat_rot_ = true;
	_delay_ms(500);
	changerVitesseTra1();
	translater_bloc(220.0);
	tourner_bloc(PI/2);
	translater_bloc(-1000.0);
	etat_rot_ = false;
	changerVitesseTra2();
	translater_bloc(-300.0);
	y(LARGEUR_ROBOT/2);
	changer_orientation(PI/2);
	etat_rot_ = true;
	_delay_ms(500);
	changerVitesseTra1();
	translater_bloc(150.0);
	if (couleur_ == 'r') tourner_bloc(0.0); else tourner_bloc(PI);
// 	etat_rot_ = false;
// 	etat_tra_ = false;
	changerVitesseTra2();
	changerVitesseRot1();
	_delay_ms(200);
	serial_t_::print("FIN_REC");
}

void Robot::translater_bloc(float distance)
{
	translater(distance);
	while(not est_stoppe() && not est_bloque_){
		asm("nop");
	}
}

void Robot::tourner_bloc(float angle)
{
	tourner(angle);
	while(not est_stoppe() && not est_bloque_){
		asm("nop");
	}
}
