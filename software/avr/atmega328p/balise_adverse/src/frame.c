#include "frame.h"


void sendData(uint16_t distance)
{
	uint16_t data = distance;
	
	//Le 16e bit du contennu indentifie le robot
	if(ROBOT==PETIT_ROBOT)
		data |= (1 << 15);
	else
		data &= ~(1 << 15);
	
	Serial<0>::print(data);
	
	//Calcul du CRC
// 	Serial<0>::print(crc8(data));
}

Frame makeFrame(uint16_t distance)
{
	Frame frame=0;
	Crc crc=0;
	Data data = distance;
	
	//Le 16e bit du contennu indentifie le robot
	if(ROBOT==PETIT_ROBOT)
		data |= (1 << 15);
	else
		data &= ~(1 << 15);
	
	//Calcul du CRC
	crc = crc8(data);
	//On met l'information utile en début de trame
	frame = ((uint32_t) data << 16);
	//On ajoute le CRC
	frame += ((uint16_t) crc << 8);
	//On ajoute le caractère de terminaison
	//frame += '\n';
	
	return frame;
}

void sendFrame(Frame frame)
{
	Serial<0>::print(frame);
}
