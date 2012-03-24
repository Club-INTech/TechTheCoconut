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
		robot.envoyer_acquittement();
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

	robot.atteinteConsignes();
	robot.gestionStoppage();
	
	robot.asservir();
	robot.updatePosition();
	
}
