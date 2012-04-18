/**
 * \file frame.cpp
 */

#include "frame.h"
#include <libintech/serial/serial_0.hpp>

Frame::Frame(uint32_t rawFrame) {
	 
	data_ = (uint16_t) (rawFrame >> 16);
	crc_ = (uint8_t) (rawFrame >> 8);
	//Récupération du bit robot
	robotId_ = (unsigned char) (data_ >> 15);
	//Mise à 0 du bit identifiant le robot
	distance_ = (uint16_t) (data_ & ~(1 << (15)));
}

bool Frame::isValid() {
	return (crc8(data_)==crc_);
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
