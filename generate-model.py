#!/usr/bin/python

import cjson
import gflags
import glob
import leveldb
import sys
import os.path
import chess_util

FLAGS = gflags.FLAGS

gflags.DEFINE_string('analysis', 'd13.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))

(hit, miss, n_best_move, n_not_best_move) = (0, 0, 0, 0)

class Position(object):
    def __init__(self, mp):
        self._map = mp

    fen = property(lambda me: me._map['fen'])
    move = property(lambda me: me._map['move'])
    san = property(lambda me: me._map['san'])
    ply = property(lambda me: me._map['ply'])
    num_legal_moves = property(lambda me: me._map['num_legal_moves'])    

class Game(object):
    def __init__(self, f):
        self._map = cjson.decode(f.read())
        
    positions = property(lambda me: (Position(pos) for pos in me._map['positions']))
    event = property(lambda me: me._map['event'])    
    black_elo = property(lambda me: me._map['black_elo'])
    white_elo = property(lambda me: me._map['white_elo'])
    game_ply = property(lambda me: me._map['game_ply'])
    result = property(lambda me: me._map['result'])
    is_mate = property(lambda me: me._map['is_mate'])
    is_stalemate = property(lambda me: me._map['is_stalemate'])

class GameAnalysis(object):
    def __init__(self, mp):
        self._map = mp
        
    depth = property(lambda me: me._map['depth'])
    moves = property(lambda me: me._map['moves'])
    analysis = property(lambda me: (Analysis(a) for a in me._map['analysis']))
    extra = property(lambda me: me._map['extra'])

class Analysis(object):
    def __init__(self, mp):
        self._map = mp
        
    depth = property(lambda me: me._map['depth'])
    score = property(lambda me: me._map['score'])
    pv = property(lambda me: me._map['pv'])
    nodes = property(lambda me: me._map['nodes'])
    multipv = property(lambda me: me._map['multipv'])    

def ProcessFile(db, fn):
    global hit, miss, n_best_move, n_not_best_move
    with file(fn) as f:
        game = Game(f)
        print 'pos', game.event, game.white_elo, game.black_elo, game.game_ply, game.result

        for pos in game.positions:
            simple = chess_util.SimplifyFen(pos.fen)

            try:
                raw = db.Get(simple)
                hit += 1
            except KeyError:
                miss += 1
                continue
            analysis = GameAnalysis(cjson.decode(raw))
            target_depth = analysis.depth
            for line in analysis.analysis:
                if line.depth != target_depth:
                    continue
                best_line = line
                break

            best_pv = best_line.pv
            best_move = best_pv[0]
            if pos.move == best_move:
                n_best_move += 1
            else:
                n_not_best_move += 1



def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    db = leveldb.LevelDB(FLAGS.analysis)
    files = 0
    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)
        
    for fn in argv[1:]:
        if os.path.isdir(fn):
            for fn in glob.glob(fn + '/*.json'):
                ProcessFile(db, fn)
                files += 1
        else:
            ProcessFile(db, fn)
            files += 1
    print "Hit:            ", hit
    print "Miss:           ", miss
    print "Best move:      ", n_best_move
    print "Not best move:  ", n_not_best_move    
    print "Files:          ", files

if __name__ == '__main__':
    main(sys.argv)        
