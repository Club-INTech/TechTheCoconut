CC=avr-gcc
CFLAGS=-Wall -O2 
MMCU_GCC=atmega328p
MMCU_DUDE=m328p
FREQ=16000000

all: clean main.hex

main.hex: main.out
	avr-objcopy -O ihex -R .eeprom main.out main.hex

main.out: main.o ax12.o actionneurs.o
	$(CC) $(CFLAGS) -mmcu=$(MMCU_GCC) -DF_CPU=$(FREQ) main.o ax12.o actionneurs.o -o main.out

%.o: %.c
	$(CC) $(CFLAGS) -mmcu=$(MMCU_GCC) -DF_CPU=$(FREQ) -c $<

clean:
	rm -rf *.o *.hex *.out *~

upload: all
	sudo avrdude -P /dev/ttyUSB0 -c stk500v1 -p $(MMCU_DUDE) -b 57600 -D -U flash:w:main.hex

upload2: all
	sudo avrdude -c usbasp -p $(MMCU_DUDE) -U flash:w:main.hex

upload3: all
	sudo avrdude -c usbtiny -p $(MMCU_DUDE) -U flash:w:main.hex