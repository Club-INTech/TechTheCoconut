CROSS_COMPILE=avr-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJ=$(CROSS_COMPILE)objcopy

MMCU=atmega328p
F_CPU=16000000
LDFLAGS=
CFLAGS=-Wall -O2 -mmcu=$(MMCU)
CXXFLAGS=-Wall -O2 -mmcu=$(MMCU)
CPPFLAGS=-Iinclude -I. -DF_CPU=$(F_CPU)

SRC=src/asservissement.o src/i2c.o src/rotation.o src/serie.o src/translation.o

export CROSS_COMPILE CC CPP LD AS AR OBJ F_CPU LDFLAGS CFLAGS SRC

all: asservissement.hex

asservissement.hex: asservissement.out
	$(OBJ) -O ihex -R .eeprom asservissement.out asservissement.hex

asservissement.out: main.o $(SRC)
	$(LD) $(LDFLAGS) -o asservissement.out $(SRC) main.o

main.o: main.cpp
	$(CPP) $(CXXFLAGS) $(CPPFLAGS) -c main.cpp

$(SRC):
	$(MAKE) -C src/

clean:
	rm -rf *.o *.out *.hex
	$(MAKE) clean -C src/

.PHONY: all clean
