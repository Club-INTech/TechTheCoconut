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
				,angle_courant_(0.0)
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
// 	serial_t_::print("Debut");
	serial_t_::change_baudrate(9600);
	
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int32_t pwmTranslation = translation.pwm(distance);
	int32_t pwmRotation = rotation.pwm(angle);
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
	//serial_t_::print(rotation.pwmCourant());
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
		serial_t_::print(x());
	}
	else if(COMPARE_BUFFER("ey")){
		serial_t_::print(y());
	}
	else if(COMPARE_BUFFER("eo")){
		serial_t_::print(angle_courant()*1000);
	}
	
	else if(COMPARE_BUFFER("d")){
		translater(serial_t_::read_float());
		Serial<0>::print("END");
	}
	else if(COMPARE_BUFFER("t")){
		tourner(serial_t_::read_float());
		Serial<0>::print("END");
	}
	
	else if(COMPARE_BUFFER("goto")){
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();
		gotoPos(co_x , co_y);
		Serial<0>::print("END");
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


void Robot::gotoPos(float x, float y)
{
	
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle;
	
	/*
	if (delta_x==0)
	{
		if (delta_y > 0)
			angle=PI/2;
		else
			angle=-PI/2;
	}
	else if (delta_x > 0)
	{
		angle=atan(delta_y/delta_x);
	}
	else
	{
		if (delta_y > 0)
			angle=atan(delta_y/delta_x) - PI;
		else
			angle=atan(delta_y/delta_x) + PI;
	}
	*/
	
	angle=atan2(delta_y,delta_x);
	
	tourner(angle);
	
	translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}

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
