/**
 * \file main.cpp
 * 
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include "robot.h"
#include "communication.h"
#include <util/delay.h>


/**
 * Fonction principale
 * 
 * \return int 0 si aucune erreur, 1 si erreur
 */
int main()
{
	//Robot robot;
	uart_init();
	while(1)
	{
		_delay_ms(1000);
		printlnLong(50);
		//Communication::traiter(robot);
	}
	return 0;
}

//ISR(TIMER1_OVF_vect, ISR_NOBLOCK){
	//robot.asservir();
//}
