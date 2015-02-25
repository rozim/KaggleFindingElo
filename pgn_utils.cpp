
#include <string>

#include "string_utils.h"
#include "pgn_utils.h"
#include "board.h"
#include "fen.h"
#include "san.h"

using namespace std;

static string SimplifyFen(const string& fen) {
  StringVector sv;
  SplitStringList(fen, " ", &sv);
  CHECK(sv.size() == 6);
  string xfen;
  for (size_t i = 0; i < 4; i++) {
    xfen += sv[i];
    if (i < 3) {
      xfen += " ";
    }
  }
  return xfen;
}

static string PositionFen(const string& fen) {
  StringVector sv;
  SplitStringList(fen, " ", &sv);
  CHECK(sv.size() == 6);
  return sv[0];
}

string BoardToSimpleFen(const board_t& board) {
  char fen[123];
  CHECK(board_to_fen(&board, fen, sizeof(fen)));
  return SimplifyFen(fen);
}

string BoardToPositionFen(const board_t& board) {
  char fen[123];
  CHECK(board_to_fen(&board, fen, sizeof(fen)));
  return PositionFen(fen);
}

string BoardToFen(const board_t& board) {
  char fen[123];
  CHECK(board_to_fen(&board, fen, sizeof(fen)));
  return fen;
}

string Quote(const char * s) {
  string res;
  for (size_t i = 0; i < strlen(s); i++) {
    if (s[i] == '\\') {
      res += "\\\\";
    } else if (s[i] == '"') {
      res += "\\\"";
    } else if (s[i] == '\'') {
      res += "''"; 
    } else {
      res += s[i];
    }
  }
  return res;
}

void PrintPgnHeader(FILE * fpgn, pgn_t * pgn) {
  // sect 8.1.1 - fixed order of these 7
  // also note these are legal "!", "?", "!!", "!?", "?!", and "??"
  fprintf(fpgn, "[Event \"%s\"]\n", Quote(pgn->event).c_str());
  fprintf(fpgn, "[Site \"%s\"]\n", Quote(pgn->site).c_str());
  fprintf(fpgn, "[Date \"%s\"]\n", pgn->date);
  fprintf(fpgn, "[Round \"%s\"]\n", Quote(pgn->round).c_str());
  fprintf(fpgn, "[White \"%s\"]\n", Quote(pgn->white).c_str());
  fprintf(fpgn, "[Black \"%s\"]\n", Quote(pgn->black).c_str());
  fprintf(fpgn, "[Result \"%s\"]\n", pgn->result);
  fprintf(fpgn, "[WhiteElo \"%s\"]\n", pgn->white_elo);
  fprintf(fpgn, "[BlackElo \"%s\"]\n", pgn->black_elo);
  fprintf(fpgn, "\n");
}
