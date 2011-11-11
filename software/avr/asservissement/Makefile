all: asserv

asserv: main.o asservissement.o i2c.o rotation.o serie.o translation.o
	g++ main.o asservissement.o i2c.o rotation.o serie.o translation.o -o asserv

main.o: main.cpp
	g++ -c main.cpp

asservissement.o: ./src/asservissement.cpp
	g++ -c ./src/asservissement.cpp

i2c.o: ./src/i2c.cpp
	g++ -c ./src/i2c.cpp

serie.o: ./src/serie.cpp
	g++ -c ./src/serie.cpp

translation.o: ./src/i2c.cpp
	g++ -c ./src/translation.cpp

rotation.o: ./src/rotation.cpp
	g++ -c ./src/rotation.cpp

clean:
	rm -rf *o asserv