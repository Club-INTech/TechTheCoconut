PROJECT_FILE=$(subst src/,,$(SRC))
CPPFLAGS=-I../include -I.


all: $(PROJECT_FILE)

%.o: %.cpp
	$(CPP) $(CXXFLAGS) $(CPPFLAGS) -c $<

clean:
	rm *.o

.PHONY: all clean
