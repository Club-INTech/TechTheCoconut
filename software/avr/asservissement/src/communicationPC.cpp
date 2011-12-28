/**
 * \file communicationPC.cpp
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

	void traiterCaractere(unsigned char caractereLu,Robot &robot)
	{
		switch (caractereLu)
		{
			case '?':
				// Ping de la liason serie
				printUShort(0);
				break;
			case 'a':
				
				break;
			case 'b':
				
				break;
			case 'c':
				traiterCaractereC(lireCaractere(),robot);
				break;
			case 'g':
				
				break;
			case 'h':
				
				break;
			case 'i':
				
				break;
			case 'j':
				
				break;
			case 'l':
				
				break;
			case 'o':
				desactiverOverflowInterruptTimerTIMSK1();
				break;
			case 'p':
				traiterCaractereP(lireCaractere(),robot);
				break;
			case 'q':
				
				break;
			case 'r':
				
				break;
			case 's':
				
				break;
			case 't':
				
				break;
			case 'u':
				
				break;
			case 'x':
				traiterCaractereX(lireCaractere(),robot);
				break;
			case 'y':
				traiterCaractereY(lireCaractere(),robot);
				break;
			case 'z':
			
				break;
			default:
				break;
		}
	}

	void traiterCaractereC(unsigned char caractereLu,Robot &robot)
	{
		switch (caractereLu)
		{
			case 't':
				traiterCaractereCT(lireCaractere(),robot);
				break;
			case 'r':
				traiterCaractereCR(lireCaractere(),robot);
				break;
			default:
				break;
		}
	}


	void traiterCaractereCT(unsigned char caractereLu,Robot &robot)
	{
		int32_t i=0;
		switch (caractereLu)
		{
			case 'p':
				i=lireEntierLong();
				// if (i >= 0) translation.asservissement_.Kp(i);
				break;
			case 'd':
				i=lireEntierLong();
				// if (i >= 0) robot.translation.asservissement_.Kd(i);
				break;
			case 'i':
				i=lireEntierLong();
				// if (i >= 0) robot.translation.asservissement_.Ki(i);
				break;
			default:
				break;
		}
	}

	void traiterCaractereCR(unsigned char caractereLu,Robot &robot)
	{
		int32_t i=0;
		switch (caractereLu)
		{
			case 'p':
				i=lireEntierLong();
				// if (i >= 0) robot.rotation.asservissement_.Kp(i);
				break;
			case 'd':
				i=lireEntierLong();
				// if (i >= 0) robot.rotation.asservissement_.Kd(i);
				break;
			case 'i':
				i=lireEntierLong();
				// if (i >= 0) robot.rotation.asservissement_.Ki(i);
				break;
			default:
				break;
		}
	}

	void traiterCaractereP(unsigned char caractereLu,Robot &robot)
	{
		switch (caractereLu)
		{
			case 't':
				
				break;
			case 'r':
				
				break;
			default:
				break;
		}
	}

	void traiterCaractereX(unsigned char caractereLu,Robot &robot)
	{
		switch (caractereLu)
		{
			case 'g':
				
				break;
			case 's':
				
				break;
			default:
				break;
		}
	}

	void traiterCaractereY(unsigned char caractereLu,Robot &robot)
	{
		switch (caractereLu)
		{
			case 'g':
				
				break;
			case 's':
				
				break;
			default:
				break;
		}
	}

	void desactiverOverflowInterruptTimerTIMSK1()
	{
		TIMSK1 &= ~(1 << TOIE1);
	}
}