
#include "robot.h"
#include "twi_master.h"
#include <math.h>

// Constructeur avec assignation des attributs
Robot::Robot() : translation(2,0.5,0),
				rotation(2,4,0),
				couleur_('r'),
				x_(0),
				y_(0)
{
	TWI_init();
	uart_init();
	printlnString("debut");
}

int __cxa_guard_acquire(__guard *g) {return !*(char *)(g);};
void __cxa_guard_release (__guard *g) {*(char *)g = 1;};
void __cxa_guard_abort (__guard *) {};

Robot& Robot::Instance()
{
	static Robot robot;
	return robot;
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
    int16_t delta_distance = distance - last_distance;
    int16_t delta_angle = angle - last_angle;
    static const float CONVERSION_TIC_MM = 1.04195690364;
    static const float CONVERSION_TIC_RADIAN = 0.000737463064;

    if(delta_angle==0)
    {
        float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
	float last_angle_radian =  last_angle * CONVERSION_TIC_RADIAN;

	if(couleur_ == 'r')
	{
			x_ -= ( delta_distance_mm * cos( last_angle_radian ) );
			y_ += ( delta_distance_mm * sin( last_angle_radian ) );

        }
        else
        {
			x_ += ( delta_distance_mm * cos( last_angle_radian ) );
			y_ -= ( delta_distance_mm * sin( last_angle_radian ) );

	}
    }
    else
    {
        
	float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
	float delta_angle_radian = delta_angle * CONVERSION_TIC_RADIAN;
	
        float r = delta_distance_mm/delta_angle_radian;
	
	float angle_radian =  angle * CONVERSION_TIC_RADIAN;
	float last_angle_radian =  last_angle * CONVERSION_TIC_RADIAN;
	
	if(couleur_ == 'r')
	{
			x_ -= r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ += r * (cos(angle_radian) - cos(last_angle_radian));
        }
        else
        {
			x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ -= delta_distance_mm * sin(last_angle_radian);
	}
    }
    printlnLong(x_);
    last_distance = distance;
    last_angle = angle;
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
