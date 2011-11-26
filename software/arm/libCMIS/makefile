#Option de compilation
OPTIMISATION = 2
DEBUG = -g

#Flag de compilation
GCFLAGS = -Wall -fno-common -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) $(DEBUG)
#LDFLAGS = -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) -nostartfiles -wl,-Map=$(PROJECT).map -T$(LSCRIPT)

#Nom du compilateur, assembleur, linkeur, etc ...
GCC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
OBJCOPY = arm-none-eabi-objcopy
REMOVE = rm -f
SIZE = arm-none-eabi-size
AR = arm-none-eabi-ar

all: system_LPC17xx.o core_cm3.o startup_LPC17xx.o

system_LPC17xx.o: system_LPC17xx.c
	$(GCC) $(GCFLAGS) system_LPC17xx.c -c

core_cm3.o: core_cm3.c
	$(GCC) $(GCFLAGS) core_cm3.c -c

startup_LPC17xx.o: startup_LPC17xx.s
	$(AS) -mcpu=cortex-m3 -o startup_LPC17xx.o startup_LPC17xx.s

archive: all
	$(AR) -rv libCMIS.a system_LPC17xx.o core_cm3.o startup_LPC17xx.o 

clean:
	$(REMOVE) *.o *.a
