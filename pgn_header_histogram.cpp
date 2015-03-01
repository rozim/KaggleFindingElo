

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
  map<int, int> freq;
  map<int, int> freq_sum;
  map<int, int> freq_diff;
  map<int, int> freq_draw_w;
  map<int, int> freq_draw_b;
  map<int, int> freq_wwin_w;
  map<int, int> freq_wwin_b;
  map<int, int> freq_bwin_w;
  map<int, int> freq_bwin_b;
  int bad = 0;
  int good = 0;
  while (*++argv) {
    pgn_t pgn[1];
    pgn_open(pgn, *argv);

    while (pgn_next_game(pgn)) {
      int w = (atoi(pgn->white_elo) / 100) * 100;
      int b = (atoi(pgn->black_elo) / 100) * 100;
      if (w > 1000 && b > 1000 && w < 3000 && b < 3000) {
        good++;
        int sum = ((atoi(pgn->white_elo) + atoi(pgn->black_elo))/ 100) * 100;
        int diff = (abs(atoi(pgn->white_elo) - atoi(pgn->black_elo))/ 100) * 100;            
        freq[w]++;
        freq[b]++;
        freq_sum[sum]++;
        freq_diff[diff]++;
      } else {
        bad++;
      }
      board_t board; 
      board_start(&board);
      char str[256];
      while (pgn_next_move(pgn,str,256)) {
        move_do(&board, move_from_san(str, &board));
      }
    }
    pgn_close(pgn);
  }
  printf("Bad: %d\n", bad);
  printf("Good: %d\n", good);
  printf("\n");
  for (const auto it : freq) {
    printf("%4d: %6d\n", it.first, it.second);
  }
  printf("\n");
  for (const auto it : freq_sum) {
    printf("%4d: %6d\n", it.first, it.second);
  }
  printf("\n");
  for (const auto it : freq_diff) {
    printf("%4d: %6d\n", it.first, it.second);
  }
  printf("\n");    
}
