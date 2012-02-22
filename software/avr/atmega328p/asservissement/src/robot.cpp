#include <math.h>
#define PI 3.14159265

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


//techthecoconut/software/pc/lib$ rm trace_x_y;python etalonnage_constantes.py


// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
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
	serial_t_::print("Debut");
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
	float last_angle_abs;
    
	if(couleur_ == 'v')
	{
		last_angle_abs= (last_angle + 4260);
	}else{
		last_angle_abs = last_angle;
	}
	/*	
	if(delta_angle_tic==0)
	{*/
		
		float last_angle_radian = last_angle_abs* CONVERSION_TIC_RADIAN_;
		float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;
		x_ += ( delta_distance_mm * cos( last_angle_radian ) );
		y_ += ( delta_distance_mm * sin( last_angle_radian ) );
// 	}
// 	else
// 	{
//         
// 		float delta_distance_mm = delta_distance_tic * CONVERSION_TIC_MM_;
// 		float delta_angle_radian = delta_angle_tic * CONVERSION_TIC_RADIAN_;
// 		float r = delta_distance_mm/delta_angle_radian;
// 		float angle_radian =  angle * CONVERSION_TIC_RADIAN_;
// 		float last_angle_radian = last_angle_abs * CONVERSION_TIC_RADIAN_;
// 		
// 		x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
// 		y_ += r * (cos(angle_radian) - cos(last_angle_radian));
// 	}
	last_distance = distance;
	
	last_angle = angle;
}

//TODO Finir implémentation de protocole.txt
void Robot::communiquer_pc(){
	char buffer[10];
	uint8_t length = serial_t_::read(buffer,10);

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

	else if(COMPARE_BUFFER("ec")){
		serial_t_::print((char)couleur_);
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
	
	else if(COMPARE_BUFFER("ex")){
		serial_t_::print((float)x_);
	}else if(COMPARE_BUFFER("ey")){
		serial_t_::print((float)y_);
	}else if(COMPARE_BUFFER("et")){
		//TODO : orientation réelle
		serial_t_::print((float)rotation.consigne());
	}
	
// 	else if(COMPARE_BUFFER("cte")){
// 		eps_t_ = (int32_t) serial_t_::read_float();
// 	}else if(COMPARE_BUFFER("cre")){
// 		eps_r_ = (int32_t) serial_t_::read_float();
// 	}
	else if(COMPARE_BUFFER("tou")){
		tourner((int16_t)serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("tra")){
		translater((int16_t)serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("goto")){
		float co_x = serial_t_::read_float();
		float co_y = serial_t_::read_float();
// 		serial_t_::print(10);
// 		serial_t_::print(20);
		gotoPos(co_x , co_y);
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

int16_t Robot::x(void)
{
return (int16_t)x_;
}

int16_t Robot::y(void)
{
return (int16_t)y_;
}


void Robot::gotoPos(float x, float y)
{
	
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	float angle;
	
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
	
	if(couleur_=='v')
		tourner(angle - PI);
	else
		tourner(angle);
	translater(sqrt(delta_x*delta_x+delta_y*delta_y));
	
}

void Robot::translater(int16_t distance)
{	
	//Serial<0>::print(123);
	
	static int32_t eps = 20;
	translation.consigne(translation.consigne()+distance/CONVERSION_TIC_MM_);
	while(translation.est_arrive()<eps);
// 		Serial<0>::print(99999);
// 		Serial<0>::print(translation.est_arrive());
		//attend d'atteindre la consigne
}

void Robot::tourner(int16_t angle)
{

	static int32_t eps = 20;
	
	rotation.consigne(angle/CONVERSION_TIC_RADIAN_);
	while(rotation.est_arrive()<eps);
// 		Serial<0>::print(11111);
// 		Serial<0>::print(rotation.est_arrive());
		//attend d'atteindre la consigne
	
}
