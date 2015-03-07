#!/usr/bin/python

import sys
import leveldb
import cjson
import chess_util

db = leveldb.LevelDB('d1.leveldb')
fn = 'generated/game2json/%05d.json' % int(sys.argv[1])
game = cjson.decode(file(fn).read())
positions = game['positions']
for pos in positions:
    fen = pos['fen']
    si = chess_util.SimplifyFen(fen)
    a = cjson.decode(db.Get(si))
    print 'FEN: ', fen
    print a
    print
