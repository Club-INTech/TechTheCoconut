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
	
	
	//gestion de l'arret
	if (robot.demande_stop())
		robot.stopper(infos[0]);
	
	robot.asservir(infos[0],infos[1]);
	robot.updatePosition(infos[0],infos[1]);
	
	
	//detection d'un blocage - translation
	//2500 ne stoppe pas | 2000 ne démarre pas | 2200 ne stop pas ET ne démarre pas...
	if(abs(robot.tra_pwmCourant())>2200 && abs(infos[0]-robot.last_tic_tra())<2)
// 		robot.trace(abs(infos[0]-robot.last_tic_tra()));
		robot.demande_stop(true);
		
	/*
	//detection d'un blocage - rotation
	if(abs(robot.rot_pwmCourant())>200 && abs(infos[1]-robot.last_tic_rot())<50)
		robot.demande_stop(true);
	
	*/
	robot.last_tic_rot(infos[0]);
	robot.last_tic_tra(robot.last_tic_rot());
	
}
