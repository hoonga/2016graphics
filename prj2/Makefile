CPPC = g++
FLAGS = -std=c++11 -O2
GL = -lGL -lGLU -lm
GLUT = -lGL -lGLU -lglut -lm
EIGEN_DIR = ./eigen
EIGEN = -I $(EIGEN_DIR)
LIB = $(GLUT) $(EIGEN)

EXEC = ./prj

all: $(EXEC)

run: $(EXEC)
	$(EXEC)

shape: ./bin/shape.o
./bin/shape.o: ./src/shape.cpp ./src/shape.h
	$(CPPC) -c $(FLAGS) -o $@ $< $(GLUT)

branch: ./bin/branch.o
./bin/branch.o: ./src/branch.cpp ./src/branch.h
	$(CPPC) -c $(FLAGS) -o $@ $< $(GL)

node: ./bin/node.o
./bin/node.o: ./src/node.cpp ./src/node.h
	$(CPPC) -c $(FLAGS) -o $@ $< $(GL)

cam: ./bin/cam.o
./bin/cam.o: ./src/cam.cpp ./src/cam.h
	$(CPPC) -c $(FLAGS) -o $@ $< $(GL)

trackball: ./bin/trackball.o
./bin/trackball.o: ./src/trackball.cpp ./src/trackball.h
	$(CPPC) -c $(FLAGS) -o $@ $< $(GL) $(EIGEN)

$(EXEC) : ./src/glados.cpp ./bin/shape.o ./bin/branch.o ./bin/node.o ./bin/cam.o ./bin/trackball.o
	$(CPPC) $(FLAGS) -o $@ $^ $(LIB)

clean:
	rm -rf ./bin
	mkdir ./bin
	rm ./prj
