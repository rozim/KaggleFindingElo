#ifndef _pgn_utils_h
#define _pgn_utils_h

#include <string>
#include <vector>
#include "board.h"
#include "pgn.h"

using namespace std;

string BoardToSimpleFen(const board_t& board);
string BoardToPositionFen(const board_t& board);
string BoardToFen(const board_t& board);
void PrintPgnHeader(FILE * fpgn, pgn_t * pgn);
string Quote(const char * s);

void FindPawnLocations(const board_t* board,
                       vector<string>* w,
                       vector<string>* b);
#endif
