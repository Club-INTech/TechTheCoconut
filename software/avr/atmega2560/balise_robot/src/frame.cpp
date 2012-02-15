/**
 * \file frame.cpp
 */

#include "frame.h"
#include <stdint.h>
#include "crc8.h"
Frame::Frame(uint32_t frame) {
	
	data = (uint16_t)(frame >> 16);
	crc = (uint8_t)(frame >> 8);
	//Récupération du bit robot
	robotId = (unsigned int) (data >> 15);
	//Mise à 0 du bit identifiant le robot
	distance = (uint16_t)(data & ~(1 << (15)));
}

bool Frame::isValid() {
	return (crc8(data)==crc) && (data != 0);
}

unsigned char Frame::getRobotId() {
	return robotId;
}

uint16_t Frame::getDistance() {
	return distance;
}
