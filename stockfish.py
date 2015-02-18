#!/usr/bin/python

from chess_util import *

p = StartEngine('/home/dspencer/Stockfish/src/stockfish')

SetOption(p, 'Hash', '128')
SetOption(p, 'MultiPV', '5')
# SetFenPosition(p, 'K7/5q2/k7/8/8/8/8/8 w - - 0 1')

for line in SearchDepth(p, 10):
    print line


