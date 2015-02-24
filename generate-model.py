#!/usr/bin/python

import random
import cjson
import gflags
import glob
import leveldb
import sys
import os.path
import chess_util
from collections import namedtuple

FLAGS = gflags.FLAGS

gflags.DEFINE_string('analysis', 'd13.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))

gflags.DEFINE_string('train_output', 'latest-train.svm', '')
gflags.DEFINE_string('test_output', 'latest-test.svm', '')
gflags.DEFINE_string('model_dir', '.', '')
gflags.DEFINE_float('holdout', 0.1, '')
gflags.DEFINE_integer('limit', 1000, '')

(files, hit, miss, n_best_move, n_not_best_move) = (0, 0, 0, 0, 0)

ParseResult = {
    '1-0': 1.0,
    '0-1': -1.0,
    '1/2-1/2': 0.0
    }
ParseResultFlip = {
    '1-0': -1.0,
    '0-1': 1.0,
    '1/2-1/2': 0.0
    }

# tbd: consider namedtuple
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

GameInfo = namedtuple('GameInfo', ['event',
                                   'best_count',
                                   'best_pct',
                                   'game_ply',
                                   'white_elo',
                                   'black_elo',
                                   'result',
                                   'is_mate',
                                   'co_elo',
                                   'co_result'])    

def StudyGame(db, fn):
    global hit, miss, n_best_move, n_not_best_move
    with file(fn) as f:
        game = Game(f)
        #print 'pos', game.event, game.white_elo, game.black_elo, game.game_ply, game.result

        best_count = [0, 0]
        best_try = [0, 0]      
        for ply, pos in enumerate(game.positions):
            co = ply % 2
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
            best_try[co] += 1 
            if pos.move == best_move:
                n_best_move += 1
                best_count[co] += 1
            else:
                n_not_best_move += 1
        result = ParseResult[game.result]
        best_pct = [0.0, 0.0]
        if best_try[0] > 0:
            best_pct[0] = float(best_count[0]) / best_try[0]
        if best_try[1] > 0:
            best_pct[1] = float(best_count[1]) / best_try[1]            
        return GameInfo(game_ply = game.game_ply,
                        best_count = best_count,
                        best_pct = best_pct, 
                        event = game.event,
                        is_mate = game.is_mate,
                        white_elo = game.white_elo,
                        black_elo = game.black_elo,
                        result = ParseResult[game.result],
                        co_elo = [game.white_elo,
                                  game.black_elo],
                        co_result = [ParseResult[game.result],
                                     ParseResultFlip[game.result]])
                                     



def WriteFeatureMap(dir, pat_map):
    global last_predefined_index
    f = file(dir + '/featmap.txt', 'w')
    tmp = []
    for a, b in pat_map.iteritems():
        tmp.append((b, a))
    tmp.sort()
    for i, pat in tmp:
        if i <= last_predefined_index:
            f.write('%d\t%s\tfloat\n' % (i, pat))
        else:
            f.write('%d\t%s\ti\n' % (i, pat))
                
pat_map = {'ply': 0,
           'result': 1,
           'draw_ply': 2,
           'i_played_mate': 3,
           'i_was_mated': 4,
           'best_count': 5,
           'best_pct': 6}
           
           
last_predefined_index =  max(pat_map.values())
next_pat_index = max(pat_map.values()) + 1

def ProcessArgs(db, limit, argv):
    global files
    for fn in argv:
        if os.path.isdir(fn):
            for fn in glob.glob(fn + '/*.json'):
                yield StudyGame(db, fn)
                files += 1
                if files >= limit:
                    break
        else:
            yield StudyGame(db, fn)
            files += 1
            if files >= limit:
                break            

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    db = leveldb.LevelDB(FLAGS.analysis)

    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)

    train_out = file(FLAGS.model_dir + '/' + FLAGS.train_output, 'w')
    test_out = file(FLAGS.model_dir + '/' + FLAGS.test_output, 'w')
    
    for gi in ProcessArgs(db, FLAGS.limit, argv[1:]):
        i_was_mated = [0, 0]
        i_played_mate = [0, 0]
        if random.random() <= FLAGS.holdout:
            out = test_out
        else:
            out = train_out
        draw_ply = 0
        if gi.result == 0.0:
            draw_ply = gi.game_ply
        elif gi.is_mate:

            if gi.result == 1.0:
                i_played_mate[0] = gi.game_ply
                i_was_mated[1] = gi.game_ply
            elif gi.result == -1.0:
                i_played_mate[1] = gi.game_ply
                i_was_mated[0] = gi.game_ply
            else:
                raise AssertionError()


        for co in [0, 1]:
            out.write('%4d 0:%d 1:%.0f 2:%d 3:%d 4:%d 5:%d 6:%.2f\n' % (
                    gi.co_elo[co],
                    gi.game_ply,
                    gi.co_result[co],
                    draw_ply,
                    i_played_mate[0],
                    i_was_mated[0],
                    gi.best_count[co],
                    gi.best_pct[co]))
                      
    WriteFeatureMap(FLAGS.model_dir, pat_map)

    print
    print "Hit:            ", hit
    print "Miss:           ", miss
    print "Best move:      ", n_best_move
    print "Not best move:  ", n_not_best_move    
    print "Files:          ", files

if __name__ == '__main__':
    main(sys.argv)        
