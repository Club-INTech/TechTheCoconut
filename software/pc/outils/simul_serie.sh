#!/bin/bash

# Ce script crée une liaison série entre /dev/ttyUSB10 et /dev/ttyUSB20 avec un débit de baud de 9600

socat PTY,link=/dev/ttyUSB10,b9600 PTY,link=/dev/ttyUSB20,b9600