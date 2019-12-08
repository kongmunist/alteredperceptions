IDIR = .  
CC=g++
CFLAGS=-I$(IDIR)
ODIR=.
LDIR=../lib

LIBS=`pkg-config --cflags --libs opencv`

DEPS = ./camLib.hpp
_OBJ = camLib.o camera.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

%.o: %.cpp $(DEPS)
	$(CC) -c -std=c++14 -pthread -o $@ $< $(LIBS) $(CFLAGS) 
camera: $(OBJ)
	$(CC) -std=c++14 -pthread -o $@ $^ $(LIBS) $(CFLAGS) 
	
.PHONY: clean
clean:
	rm -f *.o camera 
