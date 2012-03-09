/**
 * \file frame.cpp
 */

#include "frame.h"


Frame::Frame(char rawFrame[3]) {
	
	data_ = (uint16_t) ((uint16_t) rawFrame[0] << 8) + rawFrame[1];
	crc_ = rawFrame[2];
	//Récupération du bit robot
	robotId_ = (unsigned char) (data_ >> 15);
	//Mise à 0 du bit identifiant le robot
	distance_ = (uint16_t)(data_ & ~(1 << (15)));
}

bool Frame::isValid() {
	return (crc8(data_)==crc_) && (data_ != 0);
}

unsigned char Frame::getRobotId() {
	return robotId_;
}

uint16_t Frame::getDistance() {
	return distance_;
}

uint8_t Frame::getCrc() {
	return crc_;
}
