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
				,last_angle_rad_(0.)
				,last_dist_mm_(0.)

{
	
	if(couleur_ == 'r')
		last_angle_rad_ = 0.;
	else
		//angle de Pi pour le robot violet
		last_angle_rad_ =  3.141592654;
	
	TWI_init();
	Serial<0>::init();
	TimerCounter_t::init();
	
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int32_t pwmTranslation = translation.pwm(distance);
// 	int32_t pwmTranslation = 0;
	int32_t pwmRotation = rotation.pwm(angle);
// 	int32_t pwmRotation = 0;
	Serial<0>::print(pwmTranslation);
 	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
 	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
}

void Robot::updatePosition(int32_t distance_tic, int32_t angle_tic)
{
    
	static int32_t last_distance_tic = 0;
	static int32_t last_angle_tic = 0;

	static const float CONVERSION_TIC_MM = 1.04195690364;
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
	
	float delta_angle_rad = (angle_tic - last_angle_tic)* CONVERSION_TIC_RADIAN;
	float delta_distance_mm = (distance_tic - last_distance_tic) * CONVERSION_TIC_MM;
    

	if(delta_angle_rad==0)
	{
		x_ += ( delta_distance_mm * cos( last_angle_rad_ ) );
		y_ += ( delta_distance_mm * sin( last_angle_rad_ ) );
	
	}
	else
	{
		float r = delta_distance_mm/delta_angle_rad;
		float angle_radian =  angle_tic * CONVERSION_TIC_RADIAN;
	
		x_ += r * (-sin(angle_radian) + sin(last_angle_rad_));
		y_ += r * (cos(angle_radian) - cos(last_angle_rad_));
	}
	
	//met à jour la distance parcourue (mm) sur le dernier segment
	last_dist_mm_ += (distance_tic - last_distance_tic) * CONVERSION_TIC_MM;
	
	last_distance_tic = distance_tic;
	
	//met à jour l'orientation (rad) connue du robot
	last_angle_rad_ +=  (angle_tic - last_angle_tic) * CONVERSION_TIC_RADIAN;
	
	last_angle_tic = angle_tic;
	
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


bool Robot::gotoPos(int16_t x, int16_t y)
{
	//pourquoi _x et _y sont en float au fait ?
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	if(tourner((uint16_t)(atan(delta_y/delta_x)-last_angle_rad_)))
	{
		if(translater((uint16_t)sqrt(delta_x*delta_x+delta_y*delta_y)))
			return true;
		else
			return false;
	}else
		return false;
}

bool Robot::translater(uint16_t distance)
{
	static float eps = 0.5;//incertitude
	last_dist_mm_ = 0.;
	translation.consigne((int32_t)distance);
	while(abs(last_dist_mm_ - distance) > eps);
		//attend d'atteindre la consigne
		//on peut rajouter un timeout pour détecter un problème
	
	return true;
}

bool Robot::tourner(uint16_t angle)
{
	static float eps = 0.001;//incertitude
	rotation.consigne((int32_t)angle);
	
	while(abs(last_angle_rad_ - angle) > eps);
		//attend d'atteindre la consigne
		//on peut rajouter un timeout pour détecter un problème
	
	return true;
}
