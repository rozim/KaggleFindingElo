
#include <set>
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

typedef vector<string> StringList;

static char kCols[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'};

// Test parser

void quit() {
  exit(100);
}

const int kMinFreq = 100;
const int kMaxFreq = 5000;
const int kMinPly = 10 * 2;
const int kMaxPly = 40 * 2;

template <class C>
static string Join(const C& c, const string& sep) {
  if (c.size() == 0) {
    return "";
  }
  string res;
  for (typename C::const_iterator it = c.begin();
       it != c.end();
       ++it) {
    res.append(*it);
    res.append(sep);
  }
  res.erase(res.size() - sep.size());
  return res;
}

static set<string> PawnFormations(board_t board) {
  StringList w, b;
  FindPawnLocations(&board, &w, &b);

  set<string> res;  
  if (w.size() == 0 || b.size() == 0) {
    return res;
  }

  for (int start_col = 0; start_col < 8-3; start_col++) {
    string acc;          
    for (int cur_col = start_col; cur_col < start_col+3; cur_col++) {
      for (size_t i = 0; i < w.size(); i++) {
        if (w[i][0] == kCols[cur_col]) {
          acc += w[i];
        }
      }
    }
    if (acc.size() == 0) {
      continue;
    } 
    acc += "|";
    int nb = 0;
    for (int cur_col = start_col; cur_col < start_col+3; cur_col++) {
      for (size_t i = 0; i < b.size(); i++) {
        if (b[i][0] == kCols[cur_col]) {
          acc += b[i];
          nb++;
        }
      }
    }
    if (nb == 0) {
      continue;
    }
    res.insert(acc);
  }
  return res;
}

int main(int argc, char * argv[]) {
  polyglot_init();

  map<string, int> freq;
  map<string, set<string> > ii;
  int event = 0;
  while (*++argv) {
    event++;
    pgn_t pgn[1];
    pgn_open(pgn, *argv);

    while (pgn_next_game(pgn)) {
      board_t board; 
      board_start(&board);
      char str[256];
      int ply = 0;

      set<string> game_patterns;
      while (pgn_next_move(pgn,str,256)) {
        int move = move_from_san(str, &board);
        CHECK(move != MoveNone);
        move_do(&board, move);
        if (event <= 25000 && ply >= kMinPly && ply <= kMaxPly) { 
          for (const auto& cur : PawnFormations(board)) {
            game_patterns.insert(cur);
          }
        }
        ply++;
      }
      printf("%s %zu\n", pgn->event, game_patterns.size());
      ii[pgn->event] = game_patterns;
      for (const auto& pat : game_patterns) {
        freq[pat]++;
      }
    }
    pgn_close(pgn);
  }

  set<string> good;
  for (const auto& it : freq) {
    if (it.second >= kMinFreq && it.second <= kMaxFreq) {
      //printf("%s : %d\n", it.first.c_str(), it.second);
      good.insert(it.first);
    }
  }

  FILE * f = fopen("pawn_formations.txt", "w");  
  for (const auto& it : ii) {
    vector<string> my_good;
    for (const auto& pat : it.second) {
      if (good.count(pat) == 1) {
        my_good.push_back(pat);
      }
    }


    fprintf(f, "%s:%s\n",
           it.first.c_str(),
           Join(my_good, ",").c_str());
  }
  fclose(f);
}
