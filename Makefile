

POLYGLOT = polyglot_14/src

CXX = g++ -std=c++11
CXXFLAGS += -O
CXXFLAGS += -I${POLYGLOT}
LDFLAGS += ${POLYGLOT}/polyglot.a

OBJ = pgn_utils.o string_utils.o

first : filter_pgn position_frequency pgn_header_histogram pgn_headers_to_csv game_stages

filter_pgn : filter_pgn.o ${OBJ}
	${CXX} ${LDFLAGS} filter_pgn.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

position_frequency : position_frequency.o ${OBJ}
	${CXX} ${LDFLAGS} position_frequency.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

pgn_header_histogram : pgn_header_histogram.o ${OBJ}
	${CXX} ${LDFLAGS} pgn_header_histogram.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

pgn_headers_to_csv : pgn_headers_to_csv.o ${OBJ}
	${CXX} ${LDFLAGS} pgn_headers_to_csv.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

game_stages : game_stages.o ${OBJ}
	${CXX} ${LDFLAGS} game_stages.o ${OBJ} ${POLYGLOT}/polyglot.a -o ${@}

${OBJ} :

clean :
	rm -f *.o *.a
	rm -f filter_pgn position_frequency  pgn_header_histogram pgn_headers_to_csv game_stages

