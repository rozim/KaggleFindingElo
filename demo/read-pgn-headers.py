#!/usr/bin/python

import chess.pgn
import sys

for fn in sys.argv[1:]:
    for offset, headers in chess.pgn.scan_headers(file(fn)):
        print headers['Event'],headers['WhiteElo'],headers['BlackElo'],headers['Result']
    
