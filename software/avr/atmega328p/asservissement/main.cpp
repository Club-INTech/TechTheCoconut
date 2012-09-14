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
	Robot & robot = Robot::Instance();
	
	
	if (robot.BASCULE())
		robot.bandeArcade();
	else
	{
		//mise à jour des attribut stockant la distance parcourue en tic et l'angle courant en tic
		int32_t infos[2];
		get_all(infos);
		robot.mesure_distance(infos[0]);
		robot.mesure_angle(infos[1]);
		
		//mise à jour du pwm envoyé aux moteurs pour l'asservissement
		robot.asservir();
		
		//vérification des conditions de bloquage du robot
		robot.gestion_blocage();
		
		//calcul de la nouvelle position courante du robot, en absolu sur la table (mm et radians)
		robot.update_position();
	}
}
