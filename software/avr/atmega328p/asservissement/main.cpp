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


int8_t inc = 0;

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
	
	
	Robot & robot = Robot::Instance();
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
	get_all(infos);
	
	robot.mesure_distance(infos[0]);
	robot.mesure_angle(infos[1]);

	robot.atteinte_consignes();
	robot.gestion_stoppage();
	
	robot.asservir();
	robot.update_position();
	
	
	/*
	if (inc > 5)
	{
		//boucle d'envoi d'acquittement, en cas de perte sur la série
		robot.envoyer_acquittement();
		inc = 0;
	}
	
	else
	{
		//mise à jour de la position réelle du robot dans la console python
		robot.envoyer_position();
		
		//pour étalonnage
// 		robot.envoyer_position_tic();
		
		inc++;
	}
	*/
	
	
}
