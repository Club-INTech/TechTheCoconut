/**
 * \file main.cpp
 * 
 * Fichier principal qui sert juste à appeler les fichiers, créer la structure Robot et faire le traitement du port série
 */

#include "i2c.h"
#include "serie.h"
#include "rotation.h"
#include "translation.h"

//Structure permettant d'instancier les classes
struct Robot { Serie serie; I2c i2c; Translation translation; Rotation rotation;};

/**
 * Fonction principale
 * 
 * \return int 0 si aucune erreur, 1 si erreur
 */
int main()
{
	Robot robot;
	
	while(1)
	{
		robot.serie.traiter();
	}
	return 0;
}
