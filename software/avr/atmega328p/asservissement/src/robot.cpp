#include <math.h>

#define PI 3.14159265
#define LARGEUR_ROBOT 200.0
#define LONGUEUR_TABLE 3000.0

#include "twi_master.h"
#include <libintech/serial/serial_0.hpp>
#include "robot.h"
#include <libintech/asservissement.hpp>


// Constructeur avec assignation des attributs
Robot::Robot() : 		pwmG_(0)
				,pwmD_(0)
				
{
	TWI_init();
	serial_t_::init();
	TimerCounter_t::init();
	serial_t_::change_baudrate(9600);
}

void Robot::bandeArcade()
{
	moteurGauche.envoyerPwm(pwmG_);
	moteurDroit.envoyerPwm(pwmD_);
}


////////////////////////////// PROTOCOLE SERIE ///////////////////////////////////
void Robot::communiquer_pc(){
	char buffer[17];
	serial_t_::read(buffer,17);

#define COMPARE_BUFFER(string,len) strncmp(buffer, string, len) == 0 && len>0
	if(COMPARE_BUFFER("?",1)){
		serial_t_::print(0);
	}
	
	else if(COMPARE_BUFFER("pwmG",4)){
		pwmG_ = ((int32_t) serial_t_::read_float());
	}
	else if(COMPARE_BUFFER("pwmD",4)){
		pwmD_ = ((int32_t) serial_t_::read_float());
	}
	

#undef COMPARE_BUFFER
}