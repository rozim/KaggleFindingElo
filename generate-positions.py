#!/usr/bin/python

import cjson
import sys
import collections
import chess_util
import os.path
import glob

m = collections.defaultdict(set)

def ProcessFile(fn, m):
    with file(fn) as f:
        obj = cjson.decode(f.read())
        for ply, pos in enumerate(obj['positions']):
            if pos['num_legal_moves'] > 1:
                m[chess_util.SimplifyFen(pos['fen'])].add(pos['move'])    

for fn in sys.argv[1:]:
    if os.path.isdir(fn):
        for fn in glob.glob(fn + '/*.json'):
            ProcessFile(fn, m)
    else:
        ProcessFile(fn, m)

for fen, moves in m.iteritems():
    print '%s,%s' % (fen, ':'.join(moves))

