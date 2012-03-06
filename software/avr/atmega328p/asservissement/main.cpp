/**
 * \file main.cpp
 *
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include <util/delay.h>
#include <avr/interrupt.h>

#include "twi_master.h"

#include <libintech/serial/serial_0_interrupt.hpp>
#include <stdint.h>
#include "robot.h"


int main()
{
    Robot & robot = Robot::Instance();
	while(1)
	{
 		robot.communiquer_pc();
	}
	return 0;
}

ISR(TIMER1_OVF_vect, ISR_NOBLOCK){
	/*
	Robot & robot = Robot::Instance();
	
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
	get_all(infos);
	robot.asservir(infos[0],infos[1]);
	robot.updatePosition(infos[0],infos[1]);
	*/
	
	
	//méthodes non bloquantes :
	
	Robot & robot = Robot::Instance();
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
	get_all(infos);
	
	if (abs(robot.rot_pwmCourant())>=10)
		robot.rotation_en_cours(true);

	if (robot.rotation_en_cours() && abs(robot.rot_pwmCourant())<10)
	{
		
		robot.rotation_en_cours(false);
		robot.fin_tourner();
	}
	
	if (abs(robot.tra_pwmCourant())>=10)
		robot.translation_en_cours(true);

	if (robot.translation_en_cours() && abs(robot.tra_pwmCourant())<10)
	{
		robot.translation_en_cours(false);
		robot.fin_translater();
	}
	
	
	if (robot.demande_stop())
		robot.stopper(infos[0]);
	
	robot.asservir(infos[0],infos[1]);
	robot.updatePosition(infos[0],infos[1]);
	
	
	
}
