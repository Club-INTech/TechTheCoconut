PROJECT_FILE=$(subst ../library/intech/,,$(LIB_INTECH_OBJ))
CPPFLAGS=-I../../asservissement/include -I../libavr -I../libavr/conf -I. -DF_CPU=$(F_CPU)


all: $(PROJECT_FILE)

%.o: %.c
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o

.PHONY: all clean
