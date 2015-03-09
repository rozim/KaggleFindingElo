#!/usr/bin/python

import chess_util
import cjson
import gflags
import glob
import leveldb
import numpy
import os.path
import sets
import sys

from collections import namedtuple

FLAGS = gflags.FLAGS

gflags.DEFINE_string('analysis2', 'd2.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))
gflags.DEFINE_string('analysis3', 'd3.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))
gflags.DEFINE_string('analysis13', 'd13.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))
gflags.DEFINE_string('analysis19', 'd19.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))

gflags.DEFINE_string('model_dir', '.', '')
gflags.DEFINE_integer('limit', 1000, '')

files = 0

def safe_max(ar):
    if len(ar) == 0:
        return 0
    return max(ar)

def avg(ar):
    n = len(ar)
    if n == 0:
        return 0
    return sum(ar) / float(len(ar))

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
    black_elo = property(lambda me: me._map.get('black_elo', 0))
    white_elo = property(lambda me: me._map.get('white_elo', 0))
    game_ply = property(lambda me: me._map['game_ply'])
    result = property(lambda me: me._map['result'])
    is_mate = property(lambda me: me._map['is_mate'])
    is_stalemate = property(lambda me: me._map['is_stalemate'])

class GameAnalysis(object):
    def __init__(self, mp):
        self._map = mp

    # Final depth
    depth = property(lambda me: me._map['depth'])
    moves = property(lambda me: me._map['moves'])
    # Analysis of all moves.
    # There can be multiple entries at the same depth.
    analysis = property(lambda me: (Analysis(a) for a in me._map['analysis']))
    extra = property(lambda me: me._map['extra'])

# Analysis of one move (pv[0]) at one depth
class Analysis(object):
    def __init__(self, mp):
        self._map = mp

    depth = property(lambda me: me._map['depth'])
    score = property(lambda me: me._map['score'])
    pv = property(lambda me: me._map['pv'])
    nodes = property(lambda me: me._map['nodes'])
    multipv = property(lambda me: me._map['multipv'])

# Static info about a game
GameInfo = namedtuple('GameInfo', ['event',
                                   'game_ply',
                                   'white_elo',
                                   'black_elo',
                                   'result',
                                   'is_mate',
                                   'co_elo',
                                   'co_deltas_d2',
                                   'co_deltas_d3',                                   
                                   'co_deltas_d13',
                                   'co_deltas_d19',                                   
                                   'co_scores_d2',
                                   'co_scores_d3',                                   
                                   'co_scores_d13',
                                   'co_scores_d19',                                   
                                   'co_result',
                                   'first_loss_d2',
                                   'first_loss_d3',                                   
                                   'first_loss_d13',
                                   'first_loss_d19'                                   
                                   ])

# yields ply, co, position, analysis
def GenerateAnalysis(db, game):
    for ply, pos in enumerate(game.positions):
        co = ply % 2
        simple = chess_util.SimplifyFen(pos.fen)

        try:
            raw = db.Get(simple)
        except KeyError:
            continue
        simple_pos = simple.split(' ')[0]
        analysis = GameAnalysis(cjson.decode(raw))
        yield ply, co, pos, analysis



def FindBestLine(analysis):
    move_map = {}
    best_line = None
    for i, line in enumerate(analysis.analysis):
        if line.depth != analysis.depth:
            continue
        # First line found at target depth must be the best
        if best_line is None:
            best_line = line
        move_map[line.pv[0]] = line.score
    return (best_line, move_map)

def CalculateDeltasAndScores(mega):
    deltas = [[], []]
    scores = [[], []]
    for ply, co, pos, analysis in mega:
        (best_line, move_map) = FindBestLine(analysis)
        best_move =  best_line.pv[0]
        scores[co].append([move_map[best_move], move_map[pos.move]])
        if pos.move == best_move:
            deltas[co].append(0)
        else:
            delta = abs(move_map[best_move] - move_map[pos.move])
            if delta == 0:
                # Regan gives a correction of -0.03 if an equal move was chosen
                # but which wasn't the 1st rank.
                deltas[co].append(3)
            else:
                deltas[co].append(max(3, delta))
    return deltas, scores

def CalculateFirstLoss(deltas):
    (first_loss_100, first_loss_200, first_loss_300) = (0, 0, 0)
    for ply, delta in enumerate(deltas):
        if delta >= 100 and first_loss_100 == 0:
            first_loss_100 = ply
        if delta >= 200 and first_loss_200 == 0:
            first_loss_200 = ply
        if delta >= 300 and first_loss_300 == 0:
            first_loss_300 = ply
    return (first_loss_100, first_loss_200, first_loss_300)

def StudyGame(db2, db3, db13, db19, opening_positions, fn):
    with file(fn) as f:
        game = Game(f)

        mega_d2 = list(GenerateAnalysis(db2, game))
        mega_d3 = list(GenerateAnalysis(db3, game))        
        mega_d13 = list(GenerateAnalysis(db13, game))
        mega_d19 = list(GenerateAnalysis(db19, game))        
        (deltas_d2, scores_d2) = CalculateDeltasAndScores(mega_d2)
        (deltas_d3, scores_d3) = CalculateDeltasAndScores(mega_d3)        
        (deltas_d13, scores_d13) = CalculateDeltasAndScores(mega_d13)
        (deltas_d19, scores_d19) = CalculateDeltasAndScores(mega_d19) 
        first_loss_d2 = [CalculateFirstLoss(deltas_d2[0]), CalculateFirstLoss(deltas_d2[1])]
        first_loss_d3 = [CalculateFirstLoss(deltas_d3[0]), CalculateFirstLoss(deltas_d3[1])]        
        first_loss_d13 = [CalculateFirstLoss(deltas_d13[0]), CalculateFirstLoss(deltas_d13[1])]
        first_loss_d19 = [CalculateFirstLoss(deltas_d19[0]), CalculateFirstLoss(deltas_d19[1])]        

        return GameInfo(game_ply = game.game_ply,
                        first_loss_d2 = first_loss_d2,
                        first_loss_d3 = first_loss_d3, 
                        first_loss_d13 = first_loss_d13,
                        first_loss_d19 = first_loss_d19,                        
                        co_deltas_d2 = deltas_d2,
                        co_deltas_d3 = deltas_d3,                        
                        co_deltas_d13 = deltas_d13,
                        co_deltas_d19 = deltas_d19,                        
                        co_scores_d2 = scores_d2,
                        co_scores_d3 = scores_d3,                        
                        co_scores_d13 = scores_d13,
                        co_scores_d19 = scores_d19,                        
                        event = game.event,
                        is_mate = game.is_mate,
                        white_elo = game.white_elo,
                        black_elo = game.black_elo,
                        result = ParseResult[game.result],
                        co_elo = [game.white_elo,
                                  game.black_elo],
                        co_result = [ParseResult[game.result],
                                     ParseResultFlip[game.result]])




def ProcessArgs(db2, db3, db13, db19, opening_positions, limit, argv):
    global files

    for event in range(1, limit + 1):
        fn = 'generated/game2json/%05d.json' % event
        yield StudyGame(db2, db3, db13, db19, opening_positions, fn)
        files += 1
        if files >= limit:
            break


def ReadOpeningPositions(fn):
    res = set()
    with open(fn) as f:
        for line in (line.strip() for line in f.readlines()):
            ar = line.split(',')
            res.add(ar[1].split(' ')[0]) # just position part of FEN
    return sets.ImmutableSet(res)

def ProcessDrawAndMate(gi):
    draw_ply = 0
    i_played_mate = [0, 0]
    i_was_mated = [0, 0]

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
    return (draw_ply, i_played_mate, i_was_mated)

def ProcessDeltas(gi, co, deltas):
    dampened_deltas = [min(300, delta) for delta in deltas]
    (delta_median, delta_stddev, delta_avg) = (0, 0, 0)
    if len(dampened_deltas) > 0:
        delta_avg = numpy.mean(dampened_deltas)
        delta_median = numpy.median(dampened_deltas)
        delta_stddev = numpy.std(dampened_deltas)
    return (delta_median, delta_stddev, delta_avg)

def main(argv):

    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    db2 = leveldb.LevelDB(FLAGS.analysis2, max_open_files=100)
    db3 = leveldb.LevelDB(FLAGS.analysis3, max_open_files=100)    
    db13 = leveldb.LevelDB(FLAGS.analysis13, max_open_files=100)
    db19 = leveldb.LevelDB(FLAGS.analysis19, max_open_files=100)    

    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)

    opening_positions = ReadOpeningPositions('generated/position-frequency.csv')

    for gi_num, gi in enumerate(ProcessArgs(db2, db3, db13, db19, opening_positions, FLAGS.limit, argv[1:])):
        (draw_ply, i_played_mate, i_was_mated) = ProcessDrawAndMate(gi)

        for co in [0, 1]:
            (delta_median_d2, delta_stddev_d2, delta_avg_d2) = ProcessDeltas(gi, co, gi.co_deltas_d2[co])
            (delta_median_d3, delta_stddev_d3, delta_avg_d3) = ProcessDeltas(gi, co, gi.co_deltas_d3[co])            
            (delta_median_d13, delta_stddev_d13, delta_avg_d13) = ProcessDeltas(gi, co, gi.co_deltas_d13[co])
            (delta_median_d19, delta_stddev_d19, delta_avg_d19) = ProcessDeltas(gi, co, gi.co_deltas_d19[co])            

            standard = {
                '$g_event': gi.event,
                '$g_co_rating': gi.co_elo[co],
                '$g_co': ["w", "b"][co],
                '$g_co_deltas_d2': gi.co_deltas_d2[co],
                '$g_co_deltas_d3': gi.co_deltas_d3[co],                
                '$g_co_deltas_d13': gi.co_deltas_d13[co],
                '$g_co_deltas_d19': gi.co_deltas_d19[co],                
                '$g_co_scores_d2': gi.co_scores_d2[co],
                '$g_co_scores_d3': gi.co_scores_d3[co],                
                '$g_co_scores_d13': gi.co_scores_d13[co],
                '$g_co_scores_d19': gi.co_scores_d19[co],

                'color_value': [1, -1][co],
                'game_ply': gi.game_ply,
                'result': gi.co_result[co],
                'draw_ply': draw_ply,
                'i_played_mate': i_played_mate[co],
                'i_was_mated': i_was_mated[co],
                'delta_max_d2': safe_max(gi.co_deltas_d2[co]),
                'delta_max_d3': safe_max(gi.co_deltas_d3[co]),                
                'delta_max_d13': safe_max(gi.co_deltas_d13[co]),
                'delta_max_d19': safe_max(gi.co_deltas_d19[co]),                
                'delta_avg_d2': delta_avg_d2,
                'delta_avg_d3': delta_avg_d3,
                'delta_avg_d13': delta_avg_d13,
                'delta_avg_d19': delta_avg_d19,                
                
                'delta_median_d2': delta_median_d2,
                'delta_median_d3': delta_median_d3,
                
                'delta_avg_d13': delta_avg_d13,
                'delta_median_d13': delta_median_d13,
                'delta_stddev_d13': delta_stddev_d13,
                
                'delta_avg_d19': delta_avg_d19,
                'delta_median_d19': delta_median_d19,
                'delta_stddev_d19': delta_stddev_d19,                
                
                'first_loss_100_d2': gi.first_loss_d2[co][0],
                'first_loss_200_d2': gi.first_loss_d2[co][1],
                'first_loss_300_d2': gi.first_loss_d2[co][2],
                
                'first_loss_100_d3': gi.first_loss_d3[co][0],
                'first_loss_200_d3': gi.first_loss_d3[co][1],
                'first_loss_300_d3': gi.first_loss_d3[co][2],
                
                'first_loss_100_d13': gi.first_loss_d13[co][0],
                'first_loss_200_d13': gi.first_loss_d13[co][1],
                'first_loss_300_d13': gi.first_loss_d13[co][2],

                'first_loss_100_d19': gi.first_loss_d19[co][0],
                'first_loss_200_d19': gi.first_loss_d19[co][1],
                'first_loss_300_d19': gi.first_loss_d19[co][2],                                
            }
            print cjson.encode(standard)



if __name__ == '__main__':
    main(sys.argv)



