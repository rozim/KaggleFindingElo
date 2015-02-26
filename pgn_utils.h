#ifndef _pgn_utils_h
#define _pgn_utils_h

#include <string>
using namespace std;
#include "board.h"
#include "pgn.h"

string BoardToSimpleFen(const board_t& board);
string BoardToPositionFen(const board_t& board);
string BoardToFen(const board_t& board);
void PrintPgnHeader(FILE * fpgn, pgn_t * pgn);
string Quote(const char * s);
#endif
