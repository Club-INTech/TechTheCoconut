#ifndef UTILS_H
#define UTILS_H

#define sbi(port,bit) (port) |= (1 << (bit))
#define cbi(port,bit) (port) &= ~(1 << (bit))

#endif