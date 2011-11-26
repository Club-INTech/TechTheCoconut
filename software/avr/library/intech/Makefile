PROJECT_FILE=$(subst ../library/intech/,,$(LIB_OBJ))
CPPFLAGS=-I../../asservissement/include -I. -DF_CPU=$(F_CPU)


all: $(PROJECT_FILE)

%.o: %.c
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o *.a

.PHONY: all clean
