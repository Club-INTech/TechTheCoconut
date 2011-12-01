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
CXXFLAGS=-Wall -O2 -mmcu=$(MMCU)
CPPFLAGS=-Iinclude -I. -I../library/intech -DF_CPU=$(F_CPU)

SRC=src/asservissement.o src/i2c.o src/rotation.o src/communication.o src/translation.o
LIB_OBJ=../library/intech/adc.a ../library/intech/usart.a ../library/intech/twi_master.a

export CROSS_COMPILE CC CPP LD AS AR OBJ F_CPU LDFLAGS CFLAGS CXXFLAGS SRC LIB_OBJ

all: asservissement.hex

asservissement.hex: asservissement.out
	$(OBJ) -O ihex -R .eeprom asservissement.out asservissement.hex

asservissement.out: main.o $(SRC) $(LIB_OBJ)
	$(CC) $(CPPFLAGS) $(LDFLAGS) -o asservissement.out $(SRC) $(LIB_OBJ) main.o

main.o: main.cpp
	$(CPP) $(CXXFLAGS) $(CPPFLAGS) -c main.cpp

$(SRC):
	$(MAKE) -C src/

$(LIB_OBJ):
	$(MAKE) -C ../library/intech/

clean:
	rm -rf *.o *.out *.hex
	$(MAKE) clean -C src/
	$(MAKE) clean -C ../library/intech/

.PHONY: all clean
