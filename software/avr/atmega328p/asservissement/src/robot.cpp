#include <math.h>

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include "asservissement.h"

// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
				,translation(2,0.5,0),
				rotation(2,4,0)

{
	TWI_init();
	Serial<0>::init();
}

void Robot::asservir(int32_t distance, int32_t angle)
{
	int16_t pwmTranslation = translation.pwm(distance);
	int16_t pwmRotation = rotation.pwm(angle);
	moteurDroit.envoyerPwm(pwmTranslation + pwmRotation);
	moteurGauche.envoyerPwm(pwmTranslation - pwmRotation);
}

void Robot::updatePosition(int32_t distance, int32_t angle)
{
    
    static int32_t last_distance = 0;
	static int32_t last_angle = 0;
	//Cette implémentation ne peut pas compiler (je t'explique demain pourquoi)
	//Mais l'idée est bonne :)
	
//     if(couleur_ == 'r')
// 		static int32_t last_angle = 0;
//     else
// 		//angle de Pi pour le robot violet, (en tics)
// 		static float last_angle = 4260.000001287;
// 
	int16_t delta_distance = distance - last_distance;
	int16_t delta_angle = angle - last_angle;
	static const float CONVERSION_TIC_MM = 1.04195690364;
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
    
    
    
    
//     ??
    
    float distance_mm = distance * CONVERSION_TIC_MM;
    float angle_radian = (angle + last_angle) * CONVERSION_TIC_RADIAN;
    
    x_ += ( distance_mm * cos( angle_radian ) );
    y_ += ( distance_mm * sin( angle_radian ) );
    
    
    last_distance = distance;
    last_angle = angle;

    if(delta_angle==0)
    {
        float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
	float last_angle_radian =  last_angle * CONVERSION_TIC_RADIAN;

	x_ += ( delta_distance_mm * cos( last_angle_radian ) );
	y_ += ( delta_distance_mm * sin( last_angle_radian ) );

    }
    else
    {
        
	float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
	float delta_angle_radian = delta_angle * CONVERSION_TIC_RADIAN;
	
        float r = delta_distance_mm/delta_angle_radian;
	
	float angle_radian =  angle * CONVERSION_TIC_RADIAN;
	float last_angle_radian =  last_angle * CONVERSION_TIC_RADIAN;
	
	x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
	y_ += r * (cos(angle_radian) - cos(last_angle_radian));
    }
    last_distance = distance;
    last_angle = angle;
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


	else if(COMPARE_BUFFER("crm")){
		rotation.pwmMax(serial_t_::read<uint32_t>());
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

	else if(COMPARE_BUFFER("ctm")){
		translation.pwmMax(serial_t_::read<uint32_t>());
	}
	else if(COMPARE_BUFFER("ctp")){
		translation.pwmMax(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("ctd")){
		translation.pwmMax(serial_t_::read<float>());
	}
	else if(COMPARE_BUFFER("cti")){
		translation.pwmMax(serial_t_::read<float>());
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


bool Robot::translater(uint16_t distance)
{
	return true;
}

bool Robot::tourner(uint16_t angle)
{
	return true;
}
