#include <math.h>

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


#define PI 3.14159265

//enlever
#define INITIAL 0.



// Constructeur avec assignation des attributs
Robot::Robot() : couleur_('r')
				,x_(0)
				,y_(0)
				,translation(1,1,0)
				,rotation(1.5,1,0)
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
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::print("Debut");
	serial_t_::change_baudrate(9600);
	
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
    
    
	if(delta_angle==0)
	{
		if(couleur_ == 'v')
		{
			//angle de Pi pour le robot violet (en tic)
			float last_angle_radian = (last_angle + 4260) * CONVERSION_TIC_RADIAN;
			float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
			x_ += ( delta_distance_mm * cos( last_angle_radian ) );
			y_ += ( delta_distance_mm * sin( last_angle_radian ) );
		}else{
			float last_angle_radian = last_angle* CONVERSION_TIC_RADIAN;
			float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
			x_ += ( delta_distance_mm * cos( last_angle_radian ) );
			y_ += ( delta_distance_mm * sin( last_angle_radian ) );
		}
	}
	else
	{
        
		float delta_distance_mm = delta_distance * CONVERSION_TIC_MM;
		float delta_angle_radian = delta_angle * CONVERSION_TIC_RADIAN;
		
		float r = delta_distance_mm/delta_angle_radian;
		
		float angle_radian =  angle * CONVERSION_TIC_RADIAN;
		
		if(couleur_ == 'v'){
			//angle de Pi pour le robot violet (en tic)
			float last_angle_radian = (last_angle + 4260) * CONVERSION_TIC_RADIAN;
			x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ += r * (cos(angle_radian) - cos(last_angle_radian));
		}else{
			float last_angle_radian = last_angle * CONVERSION_TIC_RADIAN;
			x_ += r * (-sin(angle_radian) + sin(last_angle_radian));
			y_ += r * (cos(angle_radian) - cos(last_angle_radian));
		}
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
	static const float CONVERSION_TIC_RADIAN = 0.000737463064;
	static const float CONVERSION_TIC_MM = 1.04195690364;
	
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
		tourner((angle-INITIAL)/CONVERSION_TIC_RADIAN - 4260);
	else
		tourner((angle-INITIAL)/CONVERSION_TIC_RADIAN);
	translater(sqrt(delta_x*delta_x+delta_y*delta_y)/CONVERSION_TIC_MM);
}

void Robot::translater(int16_t distance)
{
	static int32_t eps = 10;
	translation.consigne(translation.consigne()+distance);
	while(abs(translation.consigne() - translation.erreur()) < eps);
		//attend d'atteindre la consigne
}

void Robot::tourner(int16_t angle)
{
	static int32_t eps = 10;
	rotation.consigne(rotation.consigne()+angle);
	while(abs(rotation.consigne() - rotation.erreur()) < eps);
		//attend d'atteindre la consigne
}
