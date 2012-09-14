#include "robot.h"

// Constructeur avec assignation des attributs
Robot::Robot() : 	
			 BASCULE_(false)
			,pwmG_(0)
			,pwmD_(0)
			,couleur_('v')
			,x_(0)
			,y_(0)
			,angle_serie_(0.0)
			,angle_origine_(0.0)
			,etat_rot_(true)
			,etat_tra_(true)
			,est_bloque_(false)
			,translation(0.75,3.5,0.0)
			,rotation(0.9,3.5,0.0)
			,CONVERSION_TIC_MM_(0.10360)
			,CONVERSION_TIC_RADIAN_(0.0007117)

{
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);

	changer_orientation(PI);
	changerVitesseRot(2);
	changerVitesseTra(2);
}

void Robot::bandeArcade()
{
	moteurGauche.envoyerPwm(pwmG_);
	moteurDroit.envoyerPwm(pwmD_);
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

	float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;

	x_ += ( delta_distance_mm * cos_table(angle_serie_) );
	y_ += ( delta_distance_mm * sin_table(angle_serie_) );

	angle_serie_ += delta_angle_tic * CONVERSION_TIC_RADIAN_;

	last_distance = mesure_distance_;
	last_angle = mesure_angle_;

}

////////////////////////////// PROTOCOLE SERIE ///////////////////////////////////
void Robot::communiquer_pc(){
	char buffer[17];
	serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
	
	//ping
	if(COMPARE_BUFFER("?",1)){
		serial_t_::print(0);
	}
	
	// pour passer en mode borne d'arcade
	else if(COMPARE_BUFFER("arcade",6)){
		BASCULE_ = not BASCULE_;
	}
	else if(COMPARE_BUFFER("pwmG",4)){
		pwmG_ = ((int32_t) serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("pwmD",4)){
		pwmD_ = ((int32_t) serial_t_::read_float());
	}
	
	//couleur du robot (utile pour l'angle_origine et le recalage)
	else if(COMPARE_BUFFER("ccr",3)){
		couleur_ = 'r';
	}
	else if(COMPARE_BUFFER("ccv",3)){
		couleur_ = 'v';
	}
	else if(COMPARE_BUFFER("ec",2)){
		serial_t_::print((char)couleur_);
	}
	
	//maj des constantes d'asservissement en rotation
	else if(COMPARE_BUFFER("crp",3)){
		rotation.kp(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crd",3)){
		rotation.kd(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("cri",3)){
		rotation.ki(serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("crm",3)){
		rotation.valeur_bridage(serial_t_::read_float());
	}

	//maj des constantes d'asservissement en translation
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

	//renvoi des constantes d'asservissement en rotation
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

	//renvoi des constantes d'asservissement en translation
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

	//maj de la position absolue du robot
	else if(COMPARE_BUFFER("cx",2)){
		x_ = serial_t_::read_float();
	}
	else if(COMPARE_BUFFER("cy",2)){
		y_ =serial_t_::read_float();
	}
	else if(COMPARE_BUFFER("co",2)){
		changer_orientation(serial_t_::read_float());
	}
	
	//renvoi de la position absolue du robot
	else if(COMPARE_BUFFER("ex",2)){
		serial_t_::print((int32_t)x_);
	}
	else if(COMPARE_BUFFER("ey",2)){
		serial_t_::print((int32_t)y_);
	}
	else if(COMPARE_BUFFER("eo",2)){
		serial_t_::print((int32_t)((float)angle_serie_ * 1000));
	}

	//ordre de translation
	else if(COMPARE_BUFFER("d",1)){
		translater(serial_t_::read_float());
	}

	//ordre de rotation
	else if(COMPARE_BUFFER("t",1)){
		tourner(serial_t_::read_float());
	}

	//ordre d'arret (asservissement aux angle et position courants)
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
	}

	//demande de la position courante
	else if (COMPARE_BUFFER("pos",3)){
		serial_t_::print((int32_t)x_);
		serial_t_::print((int32_t)y_);
	}

	//vitesses prédéfinies
	else if (COMPARE_BUFFER("ctv",3))
	{
		changerVitesseTra((int16_t) serial_t_::read_float());
	}
	else if (COMPARE_BUFFER("crv",3))
	{
		changerVitesseRot((int16_t) serial_t_::read_float());
	}

#undef COMPARE_BUFFER
}
////////////////////////////// VITESSES /////////////////////////////
void Robot::changerVitesseTra(int16_t valeur)
{
	float vb_translation[] = {60.0,100.0,200.0};
	float kp_translation[] = {0.75,0.75,0.5};
	float kd_translation[] = {2.0,2.5,4.0};
	
	translation.valeur_bridage(vb_translation[valeur-1]);
	translation.kp(kp_translation[valeur-1]);
	translation.kd(kd_translation[valeur-1]);
}
void Robot::changerVitesseRot(int16_t valeur)
{
	float vb_rotation[] = {80.0,100.0,200.0};
	float kp_rotation[] = {1.5,1.2,0.9};
	float kd_rotation[] = {2.0,3.5,3.5};
	
	rotation.valeur_bridage(vb_rotation[valeur-1]);
	rotation.kp(kp_rotation[valeur-1]);
	rotation.kd(kd_rotation[valeur-1]);
}
////////////////////////////// ACCESSEURS /////////////////////////////////

bool Robot::BASCULE()
{
	return BASCULE_;
}

void Robot::mesure_angle(int32_t new_angle)
{
	mesure_angle_ = new_angle;
}
void Robot::mesure_distance(int32_t new_distance)
{
	mesure_distance_ = new_distance;
}

////////////////////////// MÉTHODES DE CALCUL ET DE DÉPLACEMENT ////////////////////////////

//calcule l'angle le plus court pour atteindre angle à partir de angleBkp (ie sans faire plusieurs tours)
// le déplacement DOIT etre relatif à angleBkp, et non pas sur un intervalle défini genre [0,2*PI[, 
// puisque angleBkp a enregistré les tours du robot sur lui meme, depuis l'initialisation.
int32_t Robot::angle_optimal(int32_t angle, int32_t angleBkp)
{
	while (angle > angleBkp+PI_TIC)
		angle -= 2*PI_TIC;
	while (angle <= angleBkp-PI_TIC)
		angle += 2*PI_TIC;
	return angle;
}

//attribuer une nouvelle orientation au robot, en radian.
// Les valeurs en tic (mesure_angle_) ne sont pas modifiées, car liées aux déplacement des codeuses.
void Robot::changer_orientation(float new_angle)
{
	int32_t new_angle_tic = angle_optimal( new_angle/CONVERSION_TIC_RADIAN_, mesure_angle_ );
	float new_angle_rad = new_angle_tic*CONVERSION_TIC_RADIAN_;

	mesure_angle_ = new_angle_tic;
	angle_origine_ = new_angle_rad - (angle_serie_ - angle_origine_);
	angle_serie_ = new_angle_rad;
}

//le robot est considéré stoppé si les vitesses sont nulles et les écarts à la consigne négligeables
bool Robot::est_stoppe()
{
	volatile bool rotation_stoppe = abs(rotation.erreur()) < 105;
	volatile bool translation_stoppe = abs(translation.erreur()) < 100;
	bool bouge_pas = rotation.erreur_d()==0 && translation.erreur_d()==0;
	return rotation_stoppe && translation_stoppe && bouge_pas;
}

void Robot::tourner(float angle)
{
	est_bloque_ = false;
	float angle_tic = (angle - angle_origine_)/CONVERSION_TIC_RADIAN_;
	rotation.consigne(angle_optimal( angle_tic, mesure_angle_ ));
	//attendre un tour de timer avant de continuer (éventuel problème avec attribut volatile)
	while(compteur.value()>0){ asm("nop"); }
}

void Robot::translater(float distance)
{
	est_bloque_ = false;
	translation.consigne(translation.consigne()+distance/CONVERSION_TIC_MM_);
	//attendre un tour de timer avant de continuer (éventuel problème avec attribut volatile)
	while(compteur.value()>0){ asm("nop"); }
}

//pour stopper le robot on l'asservit sur sa position courante
void Robot::stopper()
{
	if (not est_stoppe())
	{
		rotation.consigne(mesure_angle_);
		translation.consigne(mesure_distance_);
	}
}

void Robot::gestion_blocage()
{
	static float compteurBlocage=0;
	bool moteur_force = abs(moteurGauche.pwm()) > 45 || abs(moteurDroit.pwm()) > 45;
	bool bouge_pas = rotation.erreur_d()==0 && translation.erreur_d()==0;
	
	if (bouge_pas && moteur_force)
	{
		if(compteurBlocage==100){//20
			stopper();
			est_bloque_ = true;
			compteurBlocage=0;
		}
		else
			compteurBlocage++;
	}
	else
		compteurBlocage=0;
}

/////////////////////////// FONCTIONS BLOQUANTES POUR LE RECALAGE ///////////////////////

void Robot::recalage()
{
	changerVitesseTra(1);
	changerVitesseRot(1);
	translater_bloc(-1000.0);
	etat_rot_ = false;
	changerVitesseTra(2);
	translater_bloc(-300.0);
	if (couleur_ == 'r') x_ = (-LONGUEUR_TABLE/2+LARGEUR_ROBOT/2); else x_ = (LONGUEUR_TABLE/2-LARGEUR_ROBOT/2);
	if (couleur_ == 'r') changer_orientation(0.0); else changer_orientation(PI);
	etat_rot_ = true;
	_delay_ms(500);
	changerVitesseTra(1);
	translater_bloc(220.0);
	tourner_bloc(PI/2);
	translater_bloc(-1000.0);
	etat_rot_ = false;
	changerVitesseTra(2);
	translater_bloc(-300.0);
	y_ = (LARGEUR_ROBOT/2);
	changer_orientation(PI/2);
	etat_rot_ = true;
	_delay_ms(500);
	changerVitesseTra(1);
	translater_bloc(150.0);
	if (couleur_ == 'r') tourner_bloc(0.0); else tourner_bloc(PI);
	changerVitesseTra(2);
	changerVitesseRot(1);
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
