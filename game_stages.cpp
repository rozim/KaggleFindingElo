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

// From stockfish types.h
#if 0
  PawnValueMg   = 198,   PawnValueEg   = 258,
  KnightValueMg = 817,   KnightValueEg = 846,
  BishopValueMg = 836,   BishopValueEg = 857,
  RookValueMg   = 1270,  RookValueEg   = 1278,
  QueenValueMg  = 2521,  QueenValueEg  = 2558
const int  PawnValueMg   = 198;      
#endif

const int KnightValueMg = 817;
const int BishopValueMg = 836;
const int RookValueMg   = 1270;
const int QueenValueMg  = 2521;

const int MidgameLimit  = 15581;
const int EndgameLimit  = 3998;

bool IsEndgame(const board_t& board) {
  int wn = board.number[WhiteKnight12];
  int wb = board.number[WhiteBishop12];
  int wr = board.number[WhiteRook12];
  int wq = board.number[WhiteQueen12];

  int w = wn * KnightValueMg +
      wb * BishopValueMg +
      wr * RookValueMg +
      wq * QueenValueMg;

  int bn = board.number[BlackKnight12];
  int bb = board.number[BlackBishop12];
  int br = board.number[BlackRook12];
  int bq = board.number[BlackQueen12];

  int b = bn * KnightValueMg +
      bb * BishopValueMg +
      br * RookValueMg +
      bq * QueenValueMg;

  return ((w + b) < EndgameLimit);
}

bool IsMidgame(const board_t& board) {
  int wn = board.number[WhiteKnight12];
  int wb = board.number[WhiteBishop12];
  int wr = board.number[WhiteRook12];
  int wq = board.number[WhiteQueen12];

  int w = wn * KnightValueMg +
      wb * BishopValueMg +
      wr * RookValueMg +
      wq * QueenValueMg;

  int bn = board.number[BlackKnight12];
  int bb = board.number[BlackBishop12];
  int br = board.number[BlackRook12];
  int bq = board.number[BlackQueen12];

  int b = bn * KnightValueMg +
      bb * BishopValueMg +
      br * RookValueMg +
      bq * QueenValueMg;

  if ((b+w) <= MidgameLimit) {
    //printf("%d %d %d %d (%d) | %d %d %d %d (%d)\n",
    //wn, wb, wr, wq, w,
    //bn, bb, br, bq, b);
  }
  return ((w + b) <= MidgameLimit);
}

bool MyIsEndgame(const board_t& board) {
  int wn = board.number[WhiteKnight12];
  int wb = board.number[WhiteBishop12];
  int wr = board.number[WhiteRook12];
  int wq = board.number[WhiteQueen12];
  int wminor = wn + wb;

  int bn = board.number[BlackKnight12];
  int bb = board.number[BlackBishop12];
  int br = board.number[BlackRook12];
  int bq = board.number[BlackQueen12];
  int bminor = bn + bb;

  if (wq >= 1 && wr >= 1) { return false; }
  if (bq >= 1 && br >= 1) { return false; }  
  if (wr >= 2 && wminor >= 2) { return false; }
  if (br >= 2 && bminor >= 2) { return false; }
  /*
  printf("%d %d %d %d (%d) | %d %d %d %d (%d)\n",
         wn, wb, wr, wq, wminor,
         bn, bb, br, bq, bminor);
  */
  return true;
}

int main(int argc, char * argv[]) {
  polyglot_init();
  while (*++argv) {
    pgn_t pgn[1];
    pgn_open(pgn, *argv);

    while (pgn_next_game(pgn)) {
      int mid = 0;
      int end = 0;
      
      board_t board; 
      board_start(&board);
      char str[256];
      int ply = 0;
      while (pgn_next_move(pgn,str,256)) {
        int move = move_from_san(str, &board);
        CHECK(move != MoveNone);
        move_do(&board, move);
        ply++;
        if (mid <= 0 && ply >= 20) {
          mid = ply;
        }
        if (end <= 0 && MyIsEndgame(board)) {
          end = ply;
        }        
      }
      printf("%s,%d,%d\n",
             pgn->event,
             mid,
             end);
    }
    pgn_close(pgn);
  }
}
