#include <math.h>

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>

// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
				,translation(1,1,0)
				,rotation(1.5,1,0)
				,last_angle_tic_(0)
				,last_dist_tic_(0)

{
	
	TWI_init();
	Serial<0>::init();
	TimerCounter_t::init();
	
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int32_t pwmTranslation = translation.pwm(distance);
	int32_t pwmRotation = rotation.pwm(angle);
 	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
 	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
}


void Robot::updatePosition(int32_t distance_tic, int32_t angle_tic)
{
    

	static const float CONVERSION_TIC_MM = 1.04195690364;
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
	
	
	float delta_angle_rad = (angle_tic - last_angle_tic_)* CONVERSION_TIC_RADIAN;
	float delta_distance_mm = (distance_tic - last_dist_tic_) * CONVERSION_TIC_MM;
	
    
	
	if(delta_angle_rad==0)
	{
		if(couleur_ == 'v'){
			//angle de Pi pour le robot violet (en tic)
			float last_angle_radian = last_angle_tic_ * CONVERSION_TIC_RADIAN;
			x_ += ( delta_distance_mm * cos( last_angle_radian ) );
			y_ += ( delta_distance_mm * sin( last_angle_radian ) );
		}else{
			float last_angle_radian = (last_angle_tic_ + 4260)* CONVERSION_TIC_RADIAN;
			x_ += ( delta_distance_mm * cos( last_angle_radian ) );
			y_ += ( delta_distance_mm * sin( last_angle_radian ) );
		}
	
	}
	else
	{
		float r = delta_distance_mm/delta_angle_rad;
		float angle_radian =  angle_tic * CONVERSION_TIC_RADIAN;
	
		
		if(couleur_ == 'v'){
			//angle de Pi pour le robot violet (en tic)
			float last_angle_radian = last_angle_tic_ * CONVERSION_TIC_RADIAN;
			x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ += r * (cos(angle_radian) - cos(last_angle_radian));
		}else{
			float last_angle_radian = (last_angle_tic_ + 4260)* CONVERSION_TIC_RADIAN;
			x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ += r * (cos(angle_radian) - cos(last_angle_radian));
		}
		
		
	}
	
	//met à jour la distance parcourue
	last_dist_tic_ = distance_tic;
	
	//met à jour l'orientation du robot
	last_angle_tic_ = angle_tic;
	
}


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
		rotation.kp(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("crd")){
		rotation.kd(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("cri")){
		rotation.ki(serial_t_::read<float>());
	}

	else if(COMPARE_BUFFER("ctp")){
		translation.kp(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("ctd")){
		translation.kd(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("cti")){
		translation.ki(serial_t_::read<float>());
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


void Robot::gotoPos(int16_t x, int16_t y)
{
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
	static const float CONVERSION_TIC_MM = 1.04195690364;
	
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	
	if(couleur_=='v')
		tourner(atan2(delta_y,delta_x)/CONVERSION_TIC_RADIAN - 4260);
	else
		tourner(atan2(delta_y,delta_x)/CONVERSION_TIC_RADIAN);
	translater(sqrt(delta_x*delta_x+delta_y*delta_y)/CONVERSION_TIC_MM);
}

void Robot::translater(uint16_t distance)
{
	uint32_t cons_dist_tic = translation.consigne();
	translation.consigne((int32_t)(cons_dist_tic+distance));
	while(last_dist_tic_ != cons_dist_tic+distance);
		//attend d'atteindre la consigne
		//on peut rajouter un timeout pour détecter un problème
}

void Robot::tourner(int16_t angle)
{
	rotation.consigne((int32_t)angle);
	
	while(last_angle_tic_ != angle);
		//attend d'atteindre la consigne
		//on peut rajouter un timeout pour détecter un problème
}
