CC=avr-gcc
CFLAGS=-Wall -O2
MMCU=atmega328p
FREQ=20000000

all: main.hex

main.hex: main.out
	avr-objcopy -O ihex -R .eeprom main.out main.hex

main.out: main.o twi_slave.o compteur.o serial.o
	$(CC) $(CFLAGS) -mmcu=$(MMCU) -DF_CPU=$(FREQ) main.o twi_slave.o serial.o compteur.o -o main.out

main.o: main.c
	$(CC) $(CFLAGS) -mmcu=$(MMCU) -DF_CPU=$(FREQ) main.c -c

twi_slave.o: twi_slave.c twi_slave.h
	$(CC) $(CFLAGS) -mmcu=$(MMCU) -DF_CPU=$(FREQ) twi_slave.c -c

compteur.o: compteur.c compteur.h
	$(CC) $(CFLAGS) -mmcu=$(MMCU) -DF_CPU=$(FREQ) compteur.c -c

serial.o: serial.c serial.h
	$(CC) $(CFLAGS) -mmcu=$(MMCU) -DF_CPU=$(FREQ) serial.c -c

clean:
	rm -rf *.o *.hex *.out

upload: all
	sudo avrdude -P /dev/ttyUSB0 -c stk500v1 -p m328p -b 57600 -D -U flash:w:main.hex

upload2: all
	sudo avrdude -c usbasp -p m328p -U flash:w:main.hex

upload3: all
	sudo avrdude -c usbtiny -p m328p -U flash:w:main.hex

