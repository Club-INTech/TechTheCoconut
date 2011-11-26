PROJECT_FILE=$(subst ../library/intech/,,$(LIB_INTECH_OBJ))
CPPFLAGS=-I../../asservissement/include -I../libavr -I../libavr/conf -I. -DF_CPU=$(F_CPU)
SRC= usart.c adc.c

all: $(PROJECT_FILE)

archive: $(SRC)
	avr-ar -rv libINTech.a $(SRC)

%.o: %.c
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o *.a

.PHONY: all clean
