#!/usr/bin/python

import cjson
import sys
import collections
import chess_util

m = collections.defaultdict(set)

for fn in sys.argv[1:]:
    with file(fn) as f:
        obj = cjson.decode(f.read())
        for ply, pos in enumerate(obj['positions']):
            m[chess_util.SimplifyFen(pos['fen'])].add(pos['move'])

for fen, moves in m.iteritems():
    print '%s,%s' % (fen, ':'.join(moves))

