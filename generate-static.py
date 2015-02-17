#!/usr/bin/python

import chess.pgn
import sys

# TBD: Ply
print "#Event,WhiteElo,BlackElo,Result"
for fn in sys.argv[1:]:
    for offset, headers in chess.pgn.scan_headers(file(fn)):
        print "%s,%d,%d,%s" % (headers['Event'],
                               int(headers['WhiteElo']),
                               int(headers['BlackElo']),
                               headers['Result'])
