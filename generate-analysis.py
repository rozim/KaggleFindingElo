#!/usr/bin/python

from chess_util import *
import time

depth = 9

p = StartEngine('/home/dspencer/Stockfish/src/stockfish')

SetOption(p, 'Hash', '128')
#SetOption(p, 'MultiPV', '5')
# 
positions = 0
t1 = time.time()
for fn in sys.argv[1:]:
    with file(fn) as f:
        for line in f.readlines():
            (fen,moves) = line.split(',')
            SetFenPosition(p, fen)
            #print 'AN: ', fen
            # {'pv': ['f7f5', 'e4f5'], 'depth': '2', 'score': -32, 'time': 2, 'nodes': 223, 'multipv': 1}
            positions += 1
            for depth_report in SearchDepth(p, depth):
                #print '\t', depth_report
                pass
            if positions % 100 == 0:
                print "%d. %.1f" % (positions, time.time() - t1)
            if positions > 10000:
                break
