PROJECT_FILE=$(subst ../library/libavr/,,$(LIB_AVR_OBJ))
CPPFLAGS=-I../../asservissement/include -I../intech -Iconf -I.


all: $(PROJECT_FILE)

%.o: %.c
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o

.PHONY: all clean