#!/usr/bin/python

import chess.pgn
import sys

# Map game# to a colon-separated of positions in FEN.

print "#Event,Fen"
for fn in sys.argv[1:]:
    f = file(fn)
    while True:
        game = chess.pgn.read_game(f)

        if game is None:
            break
        headers = game.headers        
        node = game.variation(0)
        ply = 1
        fens = []
        while node.variations:
            fens.append(node.board().fen())            
            node = node.variations[0]
            ply += 1
        fens.append(node.board().fen()) # final position
        print "%s,%s" % (headers['Event'], ':'.join(fens))
