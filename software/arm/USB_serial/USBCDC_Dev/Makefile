CROSS_COMPILE=arm-none-eabi-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJCOPY=$(CROSS_COMPILE)objcopy

OPTIMISATION=0
CPPFLAGS=-Iinc -I../CMSISv2_LPC17xx/inc -L../CMSISv2_LPC17xx/ -L. -Llib -D__REDLIB__ 
#CPPFLAGS=-Iinc -Iinclude -Llib 
CFLAGS=-Wall -O$(OPTIMISATION) -fno-common -mcpu=cortex-m3 -mthumb
CXXFLAGS=-Wall -O$(OPTIMISATION)
#LDFLAGS=-Wall -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) -nostartfiles -T lib/USBCDC_Dev_Debug.ld -lCMIS
LDFLAGS=-Wall -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) -nostartfiles -lCMIS

SRC=buffer.c cdcuser.c cr_startup_lpc176x.c delay.c gpio.c pwm.c serial.c uart.c usbcore.c usbdesc.c usbhw.c usbuser.c vcomdemo.c
OBJ=buffer.o cdcuser.o cr_startup_lpc176x.o delay.o gpio.o pwm.o serial.o uart.o usbcore.o usbdesc.o usbhw.o usbuser.o vcomdemo.o
OBJ2=build/buffer.o build/cdcuser.o build/cr_startup_lpc176x.o build/delay.o build/gpio.o build/pwm.o build/serial.o build/uart.o build/usbcore.o build/usbdesc.o build/usbhw.o build/usbuser.o build/vcomdemo.o

all: USBCDC.bin USBCDC.hex

USBCDC.bin: USBCDC.elf
	$(OBJCOPY) -O binary -j .text -j .data USBCDC.elf USBCDC.bin

USBCDC.hex: USBCDC.elf
	$(OBJCOPY) -R .stack -O ihex USBCDC.elf USBCDC.hex

USBCDC.elf: $(OBJ)
	$(CC) $(CPPFLAGS) $(LDFLAGS) $(OBJ2) -o $@

%.o: src/%.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o build/$@

%.o: src/%.cpp
	$(CPP) $(CPPFLAGS) $(CXXFLAGS) -c $< -o build/$@




.PHONY: all clean

clean:
	rm -f *.hex *.elf *.bin build/*.o
