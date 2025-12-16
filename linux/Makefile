CXXFLAGS = -Wall -O3
NVCC = nvcc
LDLIBS = -lSDL2
CUDAFLAG = -O3

ifdef HEADLESS
CXXFLAGS += -DHEADLESS
CUDAFLAG += -DHEADLESS
LDLIBS =
OBJ_FILES =
endif

all: sequential cuda

sequential: sequential.cpp $(OBJ_FILES)
	$(CXX) $(CXXFLAGS) -o $@ sequential.cpp $(OBJ_FILES) $(LDLIBS)

cuda: cuda.cu $(OBJ_FILES)
	$(NVCC) $(CUDAFLAG) -o $@ cuda.cu $(OBJ_FILES) $(LDLIBS)


window.o: window.cpp window.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f cuda sequential *.o

