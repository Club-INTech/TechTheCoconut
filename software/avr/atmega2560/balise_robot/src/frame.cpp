/**
 * \file frame.cpp
 */

#include "frame.h"


Frame::Frame(uint32_t frame) {
	
	data_ = (uint16_t)(frame >> 16);
	crc_ = (uint8_t)(frame >> 8);
	//Récupération du bit robot
	robotId_ = (unsigned int) (data_ >> 15);
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
