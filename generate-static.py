#!/usr/bin/python

import chess.pgn
import sys

print "#Event,WhiteElo,BlackElo,Ply,Result"
for fn in sys.argv[1:]:
    f = file(fn)
    while True:
        game = chess.pgn.read_game(f)

        if game is None:
            print 'none'
            break
        headers = game.headers        
        node = game.variation(0)
        ply = 1
        while node.variations:
            node = node.variations[0]
            ply += 1
        try:
            print "%s,%d,%d,%d,%s" % (headers['Event'],
                                      int(headers['WhiteElo']),
                                      int(headers['BlackElo']),
                                      ply,
                                      headers['Result'])
        except KeyError:
            print "%s,,,%d,%s" % (headers['Event'],
                                  ply,
                                  headers['Result'])            
