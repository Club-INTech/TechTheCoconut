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
CPPFLAGS=-Iinclude -I. -I../library/intech -I../library/libavr -I../library/libavr/conf -DF_CPU=$(F_CPU)

SRC=src/asservissement.o src/i2c.o src/rotation.o src/serie.o src/translation.o
LIB_INTECH_OBJ=../library/intech/adc.o ../library/intech/usart.o
LIB_AVR_OBJ=../library/libavr/i2c.o ../library/libavr/i2ceeprom.o ../library/libavr/i2csw.o ../library/libavr/spi.o

export CROSS_COMPILE CC CPP LD AS AR OBJ F_CPU LDFLAGS CFLAGS CXXFLAGS SRC LIB_AVR_OBJ LIB_INTECH_OBJ

all: asservissement.hex

asservissement.hex: asservissement.out
	$(OBJ) -O ihex -R .eeprom asservissement.out asservissement.hex

asservissement.out: main.o $(SRC) $(LIB_INTECH_OBJ) $(LIB_AVR_OBJ)
	$(LD) $(LDFLAGS) -o asservissement.out $(SRC) main.o

main.o: main.cpp
	$(CPP) $(CXXFLAGS) $(CPPFLAGS) -c main.cpp

$(SRC):
	$(MAKE) -C src/

$(LIB_INTECH_OBJ):
	$(MAKE) -C ../library/intech/

$(LIB_AVR_OBJ):
	$(MAKE) -C ../library/libavr/

clean:
	rm -rf *.o *.out *.hex
	$(MAKE) clean -C src/
	$(MAKE) clean -C ../library/intech/
	$(MAKE) clean -C ../library/libavr/

.PHONY: all clean
