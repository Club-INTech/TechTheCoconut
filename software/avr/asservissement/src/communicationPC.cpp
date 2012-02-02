/**
* \file communicationPC.cpp
* 
* Communication sur la liaison série avec le PC
* 
* Remarques :
* Désactive/Active l'interupt overflow pour le timer TIMSK1 en mettant TOIE1 à 0/1.
* C'est-à-dire désactive/active les interruptions pour le timer 1
* TIMSK1 &= ~(1 << TOIE1);
* TIMSK1 |= (1 << TOIE1);
*/

#include "communicationPC.h"

namespace CommunicationPC
{
	int32_t lireEntierLong()
	{
		int32_t aux = 0;
		unsigned char j=0;
		// Sert à étager les valeurs
		int32_t k = 10000000;
		unsigned char c;
		for (j = 0; j < 8; j++) {
			while (available()==0) {
				asm("nop");
			}
			c = read();
			if (c < 48 || c > 57) {
				aux = -1;
				break;
			}
			aux += (c - 48) * k;
			k /= 10;
		}
		return aux;
	}

	unsigned char lireCaractere()
	{
		while (available() == 0) {
			asm("nop");
		}
		return read();
	}

	bool traiter(Robot &robot)
	{
		traiterCaractere(lireCaractere(),robot);
		return false;
	}

	void traiterCaractere(unsigned char caractereLu, Robot &robot)
	{
		switch (caractereLu)
		{
			case '?':
				printUShort(0);
				break;
			case 'c':
				traiterCaractereC(lireCaractere(), robot);
				break;
			case 'd':
				traiterCaractereD(lireCaractere(), robot);
				break;
			case 'e':
				traiterCaractereE(lireCaractere(), robot);
				break;
			case 'i':
				traiterCaractereI(lireCaractere(), robot);
				break;
			case 'r':
				TIMSK1 &= ~(1 << TOIE1);
				robot.translation.resetConsignes();
				robot.rotation.resetConsignes();
				TIMSK1 |= (1 << TOIE1);
				break;
			case 's':
				traiterCaractereS(lireCaractere(), robot);
				break;
			case 't':
				traiterCaractereT(lireCaractere(), robot);
				break;
			case 'x':
				traiterCaractereX(lireCaractere(), robot);
				break;
			case 'y':
				traiterCaractereY(lireCaractere(), robot);
				break;
			default:
				break;
		}
	}

	void traiterCaractereC(unsigned char caractereLu, Robot &robot)
	{
		unsigned char couleurLue;
		
		switch (caractereLu)
		{
			case 'c':
				TIMSK1 &= ~(1 << TOIE1);
				couleurLue = lireCaractere();
				if (couleurLue == 'r' || couleurLue == 'v')
					robot.couleur(couleurLue);
				TIMSK1 |= (1 << TOIE1);
				break;
			case 'm':
				traiterCaractereCM(lireCaractere(), robot);
				break;
			case 'r':
				traiterCaractereCR(lireCaractere(), robot);
				break;
			case 't':
				traiterCaractereCT(lireCaractere(), robot);
				break;
			default:
				break;
		}
	}

	void traiterCaractereCM(unsigned char caractereLu, Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		i = lireEntierLong();
		switch (caractereLu)
		{
			case 'r':
				if (i>= 0)
					robot.rotation.pwmMax(i);
				break;
			case 't':
				if (i>= 0)
					robot.translation.pwmMax(i);
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}
	
	void traiterCaractereCR(unsigned char caractereLu, Robot &robot)
	{
		int32_t i=0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'p':
				i=lireEntierLong();
				if (i >= 0)
					robot.rotation.kp(i);
				break;
			case 'd':
				i=lireEntierLong();
				if (i >= 0)
					robot.rotation.kd(i);
				break;
			case 'i':
				i=lireEntierLong();
				if (i >= 0)
					robot.rotation.ki(i);
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereCT(unsigned char caractereLu, Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'p':
				i=lireEntierLong();
				if (i >= 0)
					robot.translation.kp(i);
				break;
			case 'd':
				i=lireEntierLong();
				if (i >= 0)
					robot.translation.kd(i);
				break;
			case 'i':
				i=lireEntierLong();
				if (i >= 0)
					robot.translation.ki(i);
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereD(unsigned char caractereLu, Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'a':
				i=lireEntierLong();
				if (i >= 0)
					robot.translater(i);
				break;
			case 'r':
				i=lireEntierLong();
				if (i >= 0)
					robot.translater(-i);
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}
	
	void traiterCaractereE(unsigned char caractereLu, Robot &robot)
	{
		switch (caractereLu)
		{
			case 'c':
				TIMSK1 &= ~(1 << TOIE1);
				printlnChar(robot.couleur());
				TIMSK1 |= (1 << TOIE1);
				break;
			case 'i':
				// On ne change l'état des interruptions ici parce que c'est ce que l'on cherche à connaître
				// print 0 si interruptions sur le timer 1 désactivées
				// print 1 si interruptions sur le timer 1 activées
				printlnLong(TIMSK1 & (1 << TOIE1));
				break;
			case 'm':
				traiterCaractereEM(lireCaractere(), robot);
				break;
			case 'r':
				traiterCaractereER(lireCaractere(), robot);
				break;
			case 's':
// 				TIMSK1 &= ~(1 << TOIE1);
// 				printlnChar(robot.typeAsservissement());
// 				TIMSK1 |= (1 << TOIE1);
				break;
			case 't':
				traiterCaractereET(lireCaractere(), robot);
				break;
			default:
				break;
		}
	}

	void traiterCaractereEM(unsigned char caractereLu, Robot &robot)
	{
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'r':
				printlnLong(robot.rotation.pwmMax());
				break;
			case 't':
				printlnLong(robot.translation.pwmMax());
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}
	
	void traiterCaractereER(unsigned char caractereLu, Robot &robot)
	{
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'd':
				printlnLong(robot.rotation.kd());
				break;
			case 'i':
				printlnLong(robot.rotation.ki());
				break;
			case 'p':
				printlnLong(robot.rotation.kp());
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereET(unsigned char caractereLu, Robot &robot)
	{
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'd':
				printlnLong(robot.translation.kd());
				break;
			case 'i':
				printlnLong(robot.translation.ki());
				break;
			case 'p':
				printlnLong(robot.translation.kp());
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereI(unsigned char caractereLu, Robot &robot)
	{
		switch (caractereLu)
		{
			case 'a':
				TIMSK1 |= (1 << TOIE1);
				break;
			case 'd':
				TIMSK1 &= ~(1 << TOIE1);
				break;
			default:
				break;
		}
	}

	void traiterCaractereS(unsigned char caractereLu, Robot &robot)
	{
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'r':
// 				robot.typeAsservissement('r');
				break;
			case 't':
// 				robot.typeAsservissement('t');
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereT(unsigned char caractereLu, Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'a':
				i = lireEntierLong();
				if (i >= 0)
					robot.tourner(i);
				break;
			case 'h':
				i = lireEntierLong();
				if (i >= 0)
					robot.tourner(-i);
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereX(unsigned char caractereLu,Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'c':
				break;
			case 'e':
				printlnLong(robot.x());
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}

	void traiterCaractereY(unsigned char caractereLu,Robot &robot)
	{
		int32_t i = 0;
		TIMSK1 &= ~(1 << TOIE1);
		switch (caractereLu)
		{
			case 'c':
				break;
			case 'e':
				printlnLong(robot.y());
				break;
			default:
				break;
		}
		TIMSK1 |= (1 << TOIE1);
	}
}