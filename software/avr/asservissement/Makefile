CROSS_COMPILE=avr-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJ=$(CROSS_COMPILE)objcopy

SRC=src/asservissement.o src/i2c.o src/rotation.o src/serie.o src/translation.o

F_CPU=16000000
LDFLAGS=
CFLAGS=-Wall -O2 -DF_CPU=$(F_CPU)
CPPFLAGS=-Iinclude


all: asservissement.hex

asservissement.hex: asservissement.out
	$(OBJ) -O ihex -R .eeprom asservissement.out asservissement.hex

asservissement.out: main.o $(SRC)
	$(LD) $(LDFLAGS) -o asservissement.out $(SRC)  main.o

main.o: main.cpp
	$(CPP) $(CFLAGS) $(CPPFLAGS) -c main.cpp

$(SRC):
	make -C src/

clean:
	rm -rf *.o *.out *.hex src/*.o
