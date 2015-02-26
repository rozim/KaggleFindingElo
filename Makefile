

POLYGLOT = polyglot_14/src

CXX = g++ -std=c++11
CXXFLAGS += -O
CXXFLAGS += -I${POLYGLOT}
LDFLAGS += ${POLYGLOT}/polyglot.a

OBJ = pgn_utils.o string_utils.o

first : filter_pgn position_frequency

filter_pgn : filter_pgn.o ${OBJ}
	${CXX} ${LDFLAGS} filter_pgn.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

position_frequency : position_frequency.o ${OBJ}
	${CXX} ${LDFLAGS} position_frequency.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

${OBJ} :

clean :
	rm -f *.o *.a
	rm -f filter_pgn position_frequency

