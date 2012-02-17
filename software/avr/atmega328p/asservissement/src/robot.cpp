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

{
	
	//on peut foutre ici pour initialiser ? non ? :'( 
	//ca me semble bcp plus simple, ces valeurs initiales
	//pour gérer la couleur..
	//toute facon on a besoin de savoir la dernière orientation du robot, en attribut de classe (cf gotoPos() )

	//[Philippe]
	//Non on en a pas besoin, Il faut donner l'angle en tic par rapport à l'angle initial
	//Moi ça ne me semble pas plus simple ! Les codeuses renvoient l'angle, pas une variation d'angle
	//Et puis quoi qu'il arrive les codeuses commencent à zéro
	//Et, surtout, tu sembles oublier que le robot s'initialise AVANT la liaison série, donc que si on fait cette méthode il sera impossible de changer la couleur! :p (je viens d'y penser) [la couleur est changée depuis le script python, car on ne va pas reflasher le microcontrôleur juste avant le match]
	//Bref, je ne pense pas que ce soit une bonne idée tout compte fait
	
// 	if(couleur_ == 'r')
// 		last_angle_rad_ = 0.;
// 	else
// 		//angle de Pi pour le robot violet
// 		//Plutôt en tic
// 		last_angle_rad_ = 4259;

	
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



void Robot::updatePosition(int32_t distance, int32_t angle)
{
    
	static int32_t last_distance = 0;
	static int32_t last_angle = 0;

	int16_t delta_distance = distance - last_distance;
	int16_t delta_angle = angle - last_angle;
	static const float CONVERSION_TIC_MM = 1.04195690364;
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
    
    
	//Ton
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


//Ca n'a pas de sens de faire des fonctions qui retournent faux si elles ratent sur microcontrôleurs
//Puisque le but est de faire des fonctions qui ne ratent pas.
void Robot::gotoPos(int16_t x, int16_t y)
{
	//pourquoi _x et _y sont en float au fait ?
	//Car à chaque overflow de timer on les incrémente d'un nombre flottant
	float delta_x = (x-x_);
	float delta_y = (y-y_);
	//Penser à utiliser atan2 plutôt
	//La, tu as bien raison, suivant sa couleur, il faut ajouter ou retrancher pi
	//je l'ai juste converti en tics
	if(couleur_=='v')
		tourner((atan2(delta_y,delta_x)-4260));
	else
		tourner((atan2(delta_y,delta_x)));
	translater(sqrt(delta_x*delta_x+delta_y*delta_y));
}

void Robot::translater(int16_t distance)
{
	translation.consigne(translation.consigne()+distance);
}

void Robot::tourner(int16_t angle)
{
	rotation.consigne(angle);
}
