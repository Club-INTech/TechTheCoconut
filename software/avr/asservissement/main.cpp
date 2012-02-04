/**
 * \file main.cpp
 *
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include <util/delay.h>
#include <avr/interrupt.h>

#include <libintech/twi_master.h>
#include <libintech/usart.h>

#include "robot.h"
#include "communicationPC.h"


int main()
{
    Robot & robot = Robot::Instance();
	while(1)
	{
	}
	return 0;
}

ISR(TIMER1_OVF_vect, ISR_NOBLOCK){
	Robot & robot = Robot::Instance();
	int32_t infos[2];
	//info[0]=>distance courante ; info[1] => angle courant.
	get_all(infos);
	robot.asservir(infos[0],infos[1]);
	robot.updatePosition(infos[0],infos[1]);
	//printlnLong(robot.x());
}
