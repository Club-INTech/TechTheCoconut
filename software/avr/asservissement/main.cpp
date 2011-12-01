/**
 * \file main.cpp
 * 
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include "robot.h"
#include "communication.h"
Robot robot;

/**
 * Fonction principale
 * 
 * \return int 0 si aucune erreur, 1 si erreur
 */
int main()
{
	while(1)
	{
		Communication::traiter(robot);
	}
	return 0;
}
