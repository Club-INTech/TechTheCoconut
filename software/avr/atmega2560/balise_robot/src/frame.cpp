/**
 * \file frame.cpp
 */

#include "frame.h"
#include <libintech/serial/serial_0.hpp>

Frame::Frame(uint32_t rawFrame) {
	rawframe_=rawFrame;
	distance_ = (uint16_t) (rawFrame >> 20);//12 bits de poids les plus forts
	offset_ = (rawFrame  & 0b00000000000011111111111100000000) >> 8 ;//12 bits entre
	crc_ = (uint8_t) (rawFrame);//8 bits de poids les plus faible	
}

bool Frame::isValid() {
	return (crc8(rawframe_ && 0b11111111111111111111111100000000)==crc_);
}

uint16_t Frame::getDistance() {
	return distance_;
}

uint16_t Frame::getOffset() {
	return offset_;
}

uint8_t Frame::getCrc() {
	return crc_;
}
