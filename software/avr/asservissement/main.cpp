/**
 * \file main.cpp
 *
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include "robot.h"
#include "communicationPC.h"
#include <util/delay.h>


/**
 * Fonction principale
 *
 * \return int 0 si aucune erreur, 1 si erreur
 */


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
	robot.asservir();
}
