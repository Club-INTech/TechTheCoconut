#ifndef _FRAME_H_
#define _FRAME_H_

#include <stdint.h>
#include "utils.h"
#include "crc8.h"
#include <libintech/serial/serial_0.hpp>

Frame makeFrame(uint16_t distance, uint16_t offset);
void sendFrame(Frame frame);

#endif
