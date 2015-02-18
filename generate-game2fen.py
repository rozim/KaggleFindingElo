#!/usr/bin/python

import chess.pgn
import sys

# Map game# to a colon-separated of positions in FEN.

BoolToInt = {
    True: 1,
    False: 0}

print "#Event,Fens,Sans,Mated"
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
        sans = []
        num_legal_moves = []
        while node.variations:
            board = node.board()
            num_legal_moves.append('%d' % len(board.legal_moves))
            sans.append(node.san())
            fens.append(board.fen())            
            node = node.variations[0]
            ply += 1
        
        board = node.board()
        num_legal_moves.append('%d' % len(board.legal_moves))        
        sans.append(node.san()) # final move
        fens.append(board.fen()) # final position
        print "%s,%s,%s,%s,%d" % (headers['Event'],
                            ':'.join(fens),
                            ':'.join(sans),
                                  ':'.join(num_legal_moves),
                                  BoolToInt[board.is_checkmate()])
