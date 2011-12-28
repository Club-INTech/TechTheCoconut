PROJECT_FILE=$(subst src/,,$(SRC_OBJ))
CPPFLAGS=-I../include -I. -I../../library/intech


all: $(PROJECT_FILE)

%.o: %.cpp
	$(CPP) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o

.PHONY: all clean
