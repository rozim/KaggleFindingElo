

#include <set>
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


// Just hard code the path for now.
set<string>  ReadBlacklist() {
  set<string> res;
  FILE* f = fopen("generated/test-blacklist.txt", "r");
  char line[1024];
  while (fgets(line, sizeof line, f) != NULL) {
    line[strlen(line) - 1] = '\0'; // remove \n
    res.insert(string(line));
  }
  fclose(f);
  return res;
}

#if 0
// Just hard code the path for now.
set<string>  ReadBlacklist2() {
  set<string> res;
  FILE* b2 = fopen("b2.txt", "w");
  pgn_t pgn[1];
  pgn_open(pgn, "data/data-test.pgn");
  while (pgn_next_game(pgn)) {
    board_t board; 
    board_start(&board);
    char str[256];
    while (pgn_next_move(pgn,str,256)) {
      int move = move_from_san(str, &board);
      if (move == MoveNone || !move_is_legal(move, &board)) {
        printf("illegal move \"%s\" at line %d, column %d\n",
               str, pgn->move_line,pgn->move_column);	  
        break;
      }
      move_do(&board, move);
    }
    string pos = BoardToPositionFen(board);
    fprintf(b2, "%s\n", pos.c_str());
    res.insert(pos);
  }
  pgn_close(pgn);
  fclose(b2);
  return res;
}
#endif


int main(int argc, char * argv[]) {
  polyglot_init();
  set<string> blacklist = ReadBlacklist();

  int games = 0;
  int black = 0;
  int white = 0;

  while (*++argv) {
    printf("%s (%d %d %d)\n", *argv, black, white, games);
    pgn_t pgn[1];
    pgn_open(pgn, *argv);

    while (pgn_next_game(pgn)) {
      games++;          
      vector<string> all;      
      board_t board; 
      board_start(&board);
      char str[256];
      while (pgn_next_move(pgn,str,256)) {
        int move = move_from_san(str, &board);
        if (move == MoveNone || !move_is_legal(move, &board)) {
          printf("illegal move \"%s\" at line %d, column %d\n",
                 str, pgn->move_line,pgn->move_column);	  
	  break;
        }
        all.push_back(str);
        move_do(&board, move);
      }
      string last = BoardToPositionFen(board);
      if (blacklist.count(last) == 1) {
        black++;
        continue;
      }
      white++;
      PrintPgnHeader(stdout, pgn);
      int col = 0;
      for (int ply = 0; ply < all.size(); ply++) {
        if (ply % 2 == 0) {
          fprintf(stdout, "%d. ", (ply / 2) + 1);
          if (ply < 10) {col += 3; }
          else if (ply < 100) { col += 4; }
          else { col += 5; }
        }
        char tmp[123];
        sprintf(tmp, "%s", all[ply].c_str());
        fprintf(stdout, "%s", tmp);
        col += strlen(tmp);
        if (col >= 70) {
          fprintf(stdout, "\n");
          col = 0;
        } else {
          fprintf(stdout, " ");
          col++;
        }
      }
      fprintf(stdout, "%s\n\n", pgn->result);

    }
    pgn_close(pgn);
  }
  fprintf(stderr, "Blacklist  : %d (%zu)\n", black, blacklist.size());
  fprintf(stderr, "Whitelist  : %d\n", white);
  fprintf(stderr, "Games      : %d\n", games);  
}
