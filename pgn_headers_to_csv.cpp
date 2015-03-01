

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

int main(int argc, char * argv[]) {
  polyglot_init();
  int bad = 0, bad1 = 0, bad2 = 0, bad3 = 0;
  int good = 0;
  while (*++argv) {
    pgn_t pgn[1];
    pgn_open(pgn, *argv);

    while (pgn_next_game(pgn)) {
      int w = (atoi(pgn->white_elo) / 100) * 100;
      int b = (atoi(pgn->black_elo) / 100) * 100;

      board_t board; 
      board_start(&board);
      char str[256];
      int ply = 0;
      while (pgn_next_move(pgn,str,256)) {
        move_do(&board, move_from_san(str, &board));
        ply++;
      }
      string r(pgn->result);
      if (w > 1000 && b > 1000 && w < 3000 && b < 3000 &&
          (r == "1-0" || r == "0-1" || r == "1/2-1/2")) {
        printf("%s,%s,%s,%d\n",
               pgn->white_elo,
               pgn->black_elo,
               pgn->result,
               ply);
        good++;
      } else {
        if (!(w > 1000 && b > 1000 && w < 3000 && b < 3000)) {
          if (w == 0) {
            bad3++;
          }
          if (b == 0) {
            bad3++;
          }
          bad1++;
        }
        if (!(r == "1-0" || r == "0-1" || r == "1/2-1/2")) {
          bad2++;
        }
        bad++;
      }
    }
    pgn_close(pgn);
  }
  fprintf(stderr, "Bad: %d  bad_elo=%d  no_rat%d   no_elo=%d\n", bad, bad1, bad2, bad3);
  fprintf(stderr, "Good: %d\n", good);
}
