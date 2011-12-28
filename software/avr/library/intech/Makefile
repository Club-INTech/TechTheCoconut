PROJECT_FILE=$(subst ../library/intech/,,$(LIB_OBJ))
CPPFLAGS=-I../../asservissement/include -I. -DF_CPU=$(F_CPU)
ARFLAGS=-q

all: $(PROJECT_FILE)

%.o: %.c
	$(CC) $(CXXFLAGS) $(CPPFLAGS) -c $<

%.a: %.o
	$(AR) $(ARFLAGS) $@ $<

clean:
	rm *.a

.PHONY: all clean
