#!/usr/bin/python

import chess.pgn
import sys
import cjson
import time

def StudyGame(game):
    headers = game.headers
    node = game
    ply = 0
    positions = []
    while True:
        board = node.board()
        node = node.variations[0]        
        p = {'ply': ply,
             'num_legal_moves': len(board.legal_moves),
             'san': node.san(),
             'move': str(node.move),
             'fen': board.fen()}
        if board.is_check():
            p['in_check'] = True        
        positions.append(p)            
        ply += 1
        if not node.variations:
            break

    last_board = node.board()
    g = {
        'event': headers['Event'],
        'game_ply': ply,
        'result': headers['Result'],
        'positions': positions,
        'is_mate': last_board.is_checkmate(),
        'is_stalemate': last_board.is_stalemate()
        }
    if 'WhiteElo' in headers:
        g['white_elo'] = int(headers['WhiteElo'])
        g['black_elo'] = int(headers['BlackElo'])
    return g

t0 = time.time()
for fn in sys.argv[1:]:
    f = file(fn)
    n = 0
    mod = 1
    while True:
        game = chess.pgn.read_game(f)

        if game is None:
            break
        g = StudyGame(game)
        with file('generated/game2json/%05d.json' % int(g['event']), 'w') as cur_f:
            cur_f.write(cjson.encode(g))
        n += 1
        if n % mod == 0:
            print "%6d %.1f" % (n, time.time() - t0)
            sys.stdout.flush()
            mod *= 2


