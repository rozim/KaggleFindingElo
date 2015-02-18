#!/usr/bin/python

import chess.pgn
import sys

def ParseGames(fn):
    f = file(fn, 'r')
    while True:
        game = chess.pgn.read_game(f)
        if game is None:
            break
        else:
            yield game


def Positions(game):            
    node = game
    ar = []
    while node.variations:
        ar.append(node)
        next_node = node.variation(0)
        node = next_node
    ar.append(node)
    return ar

for fn in sys.argv[1:]:
    for game in ParseGames(fn):
        for ply, node in enumerate(Positions(game)):
            print ply, node.board().fen()
        
            
        
  
    
