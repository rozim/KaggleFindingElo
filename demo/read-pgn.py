#!/usr/bin/python

import chess.pgn
import sys

for fn in sys.argv[1:]:
    f = file(fn, 'r')
    while True:
        game = chess.pgn.read_game(f)
        if game is None:
            break
        node = game.variation(0)
        while not node.board().is_game_over():
            print 'san: ', node.san(), ' move: ', node.move, 'fen: ', node.board().fen()
            try:
                node = node.variation(0)
            except KeyError:
                break # there has to be a better way
        
    
    
