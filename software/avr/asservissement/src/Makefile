CROSS_COMPILE=avr-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJ=$(CROSS_COMPILE)objcopy

PROJECT_FILE=asservissement.o i2c.o rotation.o serie.o translation.o

F_CPU=16000000
LDFLAGS=
CFLAGS=-Wall -O2 -DF_CPU=$(F_CPU)
CPPFLAGS=-Iinclude


all: $(PROJECT_FILE)

%.o: %.cpp
	$(CPP) $(CFLAGS) $(CPPFLAGS) -c $<

clean:
	rm -rf *.o *.out *.hex
