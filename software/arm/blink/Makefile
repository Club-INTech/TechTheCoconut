CROSS_COMPILE=arm-none-eabi-
CC=$(CROSS_COMPILE)gcc
CPP=$(CROSS_COMPILE)g++
LD=$(CROSS_COMPILE)ld
AS=$(CROSS_COMPILE)as
AR=$(CROSS_COMPILE)ar
OBJCOPY=$(CROSS_COMPILE)objcopy

OPTIMISATION=0
CPPFLAGS=-Iinclude -Llib
CFLAGS=-Wall -O$(OPTIMISATION) -fno-common -mcpu=cortex-m3 -mthumb
CXXFLAGS=-Wall -O2
LDFLAGS=-Wall -mcpu=cortex-m3 -mthumb -O$(OPTIMISATION) -nostartfiles -Tlib/LPC17xx.ld -lCMIS

EXEC=blink
SRC_LIST=_main.c _blink.c
SRC=$(subst _,,$(SRC_LIST))
OBJ=$(subst .c,.o,$(SRC))
OBJ2=$(subst .c,.o,$(subst _,build/,$(SRC_LIST)))


all: $(EXEC).bin $(EXEC).hex 

$(EXEC).bin: $(EXEC).elf
	$(OBJCOPY) -O binary -j .text -j .data $(EXEC).elf $(EXEC).bin

$(EXEC).hex: $(EXEC).elf
	$(OBJCOPY) -R .stack -O ihex $(EXEC).elf $(EXEC).hex

$(EXEC).elf: $(OBJ)
	$(CC) $(CPPFLAGS) $(LDFLAGS) $(OBJ2) -o $@

%.o: src/%.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o build/$@

%.o: src/%.cpp
	$(CPP) $(CPPFLAGS) $(CXXFLAGS) -c $< -o build/$@


.PHONY: all clean

clean:
	rm -f build/* $(EXEC)*
