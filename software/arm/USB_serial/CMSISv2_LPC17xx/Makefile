CROSS_COMPILE=arm-none-eabi-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJCOPY=$(CROSS_COMPILE)objcopy

OPTIMISATION=0
CPPFLAGS=-Iinc
CFLAGS=-Wall -O$(OPTIMISATION) -fno-common -mcpu=cortex-m3 -mthumb
CXXFLAGS=-Wall -O2
LDFLAGS=-Wall -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) -nostartfiles -Tlib/LPC17xx.ld -lCMIS

all: core_cm3.o system_LPC17xx.o 

core_cm3.o: src/core_cm3.c
	$(CC) $(CPPFLAGS) $(CFLAGS) src/core_cm3.c -c

system_LPC17xx.o: src/system_LPC17xx.c
	$(CC) $(CPPFLAGS) $(CFLAGS) src/system_LPC17xx.c -c

archive: all
	$(AR) -rv libCMIS.a system_LPC17xx.o core_cm3.o

.PHONY: all clean

clean:
	rm -f *.o *.a
