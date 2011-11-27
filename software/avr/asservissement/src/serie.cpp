/**
 * \file serie.cpp
 */

#include "serie.h"

Serie::Serie()
{
	uart_init();
}

Serie::~Serie()
{
	
}

int32_t Serie::lireEntierLong()
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

unsigned char Serie::lireCaractere()
{
	while (available() == 0) {
		asm("nop");
	}
	return read();
}

bool Serie::traiter()
{
	Serie::traiterCaractere(Serie::lireCaractere());
	return false;
}

void Serie::traiterCaractere(unsigned char caractereLu)
{
	switch (caractereLu)
	{
		case '?':
			
			break;
		case 'a':
			
			break;
		case 'b':
			
			break;
		case 'c':
			traiterCaractereC(lireCaractere());
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
			
			break;
		case 'p':
			traiterCaractereP(lireCaractere());
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
			traiterCaractereX(lireCaractere());
			break;
		case 'y':
			traiterCaractereY(lireCaractere());
			break;
		case 'z':
		
			break;
		default:
			break;
	}
}

void Serie::traiterCaractereC(unsigned char caractereLu)
{
	switch (caractereLu)
	{
		case 't':
			traiterCaractereCT(lireCaractere());
			break;
		case 'r':
			traiterCaractereCR(lireCaractere());
			break;
		default:
			break;
	}
}


void Serie::traiterCaractereCT(unsigned char caractereLu)
{
	switch (caractereLu)
	{
		case 'p':
			
			break;
		case 'd':
			
			break;
		case 'i':
			
			break;
		default:
			break;
	}
}

void Serie::traiterCaractereCR(unsigned char caractereLu)
{
	switch (caractereLu)
	{
		case 'p':
			
			break;
		case 'd':
			
			break;
		case 'i':
			
			break;
		default:
			break;
	}
}

void Serie::traiterCaractereP(unsigned char caractereLu)
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

void Serie::traiterCaractereX(unsigned char caractereLu)
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

void Serie::traiterCaractereY(unsigned char caractereLu)
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