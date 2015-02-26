

#include <map>
#include <string>
#include <vector>

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#include "board.h"
#include "move.h"
#include "move_do.h"
#include "pgn.h"
#include "san.h"
#include "square.h"
#include "util.h"
#include "move_legal.h"
#include "polyglot_lib.h"
#include "utils.h"
#include "pgn_utils.h"

using namespace std;

// Test parser

void quit() {
  exit(100);
}

const int kMinFreq = 100;
const int kMaxFreq = 100000;
const int kMinPly = 5 * 2;
const int kMaxPly = 30 * 2;

int main(int argc, char * argv[]) {
  polyglot_init();
  map<string, int> freq;
  while (*++argv) {
    pgn_t pgn[1];
    pgn_open(pgn, *argv);


    while (pgn_next_game(pgn)) {
      board_t board; 
      board_start(&board);
      char str[256];
      int ply = 0;
      while (pgn_next_move(pgn,str,256)) {
        int move = move_from_san(str, &board);
        CHECK(move != MoveNone);
        move_do(&board, move);
        if (ply >= kMinPly && ply <= kMaxPly) {        
          freq[BoardToSimpleFen(board)]++;
        }
        ply++;
      }
    }
    pgn_close(pgn);
  }
  for (const auto it : freq) {
    if (it.second >= kMinFreq && it.second <= kMaxFreq) {
      printf("%d,%s\n", it.second, it.first.c_str());
    }
  }
}
