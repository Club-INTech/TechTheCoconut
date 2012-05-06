#include "crc8.h"

/*
* CRC-8-WCDMA
*/

Crc crc8_table[256];

//Fonction d'initialisation nécessaire au calcul rapide de crc
void init_crc8()
{
	int i,j;
	Crc crc;

	for (i=0; i<256; i++) 
	{
		crc = i;
		for (j=0; j<8; j++)
			crc = (crc << 1) ^ ((crc & 0x80) ? POLYNOMIAL : 0);
		crc8_table[i] = crc & 0xFF;
	}
}

//Fast CRC calculation
void crc8_byte(Crc *crc, uint8_t byte)
{
	*crc = crc8_table[(*crc) ^ byte];
	*crc &= 0xFF;
}


Crc crc8(Data data)
{
	unsigned int i,s=sizeof(data);
	Crc crc=0;
	uint8_t byte=0;
	
	for(i=s;i>0;i--)
	{
		byte = (uint8_t) (data >> 8*(i-1));
		crc8_byte(&crc,byte);
	}
	
	return crc;
}
