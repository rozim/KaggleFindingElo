#!/usr/bin/python


# TBD: w+b, w-b
# TBD: percentile

# DONE: alt_scores, mean of score in each block
# DONE: final score
# DONE: index of 1st move where ahead X (100)
# DONE debug final_score

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

gflags.DEFINE_string('analysis', 'd19.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))

gflags.DEFINE_string('game_stages', 'generated/game_stages.csv', '')

gflags.DEFINE_string('model_dir', '.', '')
gflags.DEFINE_integer('limit', 1000, '')

gflags.DEFINE_string('key_prefix', '', 'Something like d19_ to keep track of the analysis this came from')
gflags.DEFINE_bool('debug', False, '')
gflags.DEFINE_bool('verbose', False, 'More verbose data in output such as raw arrays')

# White/Black multiplier to convert scores back to white-based scores
kColorMul = { 0: 1,
              1: -1}
    
files = 0

game_stages = {} # [event] = (mg ply, eg ply)

# return dict of key=event, value= tuple (start of middle game ply, end game ply)
def ReadGameStages():
    res = {}
    for line in file(FLAGS.game_stages).read().splitlines():
        ar = line.split(',')
        res[ar[0]] = (int(ar[1]), int(ar[2]))
    return res

def safe_max(ar):
    if len(ar) == 0:
        return 0
    return max(ar)

def avg(ar):
    n = len(ar)
    if n == 0:
        return 0
    return sum(ar) / float(len(ar))

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
                                   'white_elo',
                                   'black_elo',
                                   'co_elo',

                                   'raw_scores',
                                   'co_deltas_op',
                                   'co_deltas_mg',
                                   'co_deltas_eg',
                                   'co_deltas',
                                   'co_scores',
                                   'first_loss',
                                   'final_score',
                                   'co_ply_ahead_50',
                                   'co_ply_ahead_100',

                                   'alt_stages'
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
    move_map = {} # key=move value=score
    best_line = None
    for i, line in enumerate(analysis.analysis):
        if line.depth != analysis.depth:
            continue
        # First line found at target depth must be the best
        if best_line is None:
            best_line = line
        move_map[line.pv[0]] = line.score
    return (best_line, move_map)

def CalculateDeltasAndScores(game, mega, stages):
    #print 'st', stages

    raw_scores = [[], []]
    deltas = [[], []]
    deltas_opening = [[], []]
    deltas_midgame = [[], []]
    deltas_endgame = [[], []]
    scores = [[], []]
    final_score = 0
    co_ply_ahead_50 = [0, 0]
    co_ply_ahead_100 = [0, 0]
    for ply, co, pos, analysis in mega:

        (best_line, move_map) = FindBestLine(analysis)
        
        best_move =  best_line.pv[0]
        final_score = kColorMul[co] * move_map[best_move]
        raw_scores[co].append(final_score)
        if FLAGS.debug:
            print
            print 'Analysis: ply=', ply, ' co=', co
            for a in analysis.analysis:
                print '\t', a.multipv, a.depth, a.score, a.pv
            print 'final: ', final_score
        
        if FLAGS.debug:
            print 'DBG: ',co, game.event, best_move, ply, pos.move, move_map[best_move], move_map[pos.move]        

        if co_ply_ahead_50[co] == 0 and move_map[pos.move] >= 50:
            co_ply_ahead_50[co] = ply
        if co_ply_ahead_100[co] == 0 and move_map[pos.move] >= 100:
            co_ply_ahead_100[co] = ply 
        scores[co].append([move_map[best_move], move_map[pos.move]])

        if ply <= stages[0]:
            delta2 = deltas_opening
        elif ply <= stages[1]:
            delta2 = deltas_midgame
        else:
            delta2 = deltas_endgame

        if pos.move == best_move:
            deltas[co].append(0)
            delta2[co].append(0)
        else:
            delta = move_map[best_move] - move_map[pos.move]
            if delta == 0:
                # Regan gives a correction of -0.03 if an equal move was chosen
                # but which wasn't the 1st rank.
                deltas[co].append(3)
                delta2[co].append(3)
            else:
                deltas[co].append(max(3, delta))
                delta2[co].append(max(3, delta))
    if FLAGS.debug:
        print 'Scores[0]: ', scores[0]
        print 'Deltas[0]: ', deltas[0]        
        print 'Scores[1]: ', scores[1]
        print 'Deltas[1]: ', deltas[1]

    return raw_scores, deltas, deltas_opening, deltas_midgame, deltas_endgame, scores, final_score, co_ply_ahead_50, co_ply_ahead_100

def CalculateAltStages(deltas):
    res = [ {}, {} ]
    for co in [0, 1]:
        for block in [0, 1, 2, 3, 4]:
            res[co][block] = deltas[co][block * 10 : (1 + block) * 10]
    return res

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

def StudyGame(db, fn):
    global game_stages

    with file(fn) as f:

        game = Game(f)

        stages = game_stages[game.event]

        mega = list(GenerateAnalysis(db, game))

        (raw_scores, deltas, deltas_op, deltas_mg, deltas_eg, scores, final_score, co_ply_ahead_50, co_ply_ahead_100) = CalculateDeltasAndScores(game, mega, stages)

        alt_stages = CalculateAltStages(deltas)
        
        first_loss = [CalculateFirstLoss(deltas[0]), CalculateFirstLoss(deltas[1])]

        return GameInfo(final_score = final_score,
                        raw_scores = raw_scores,
                        alt_stages = alt_stages,
                        co_ply_ahead_50 = co_ply_ahead_50, 
                        co_ply_ahead_100 = co_ply_ahead_100,
                        first_loss = first_loss,
                        co_deltas_op = deltas_op,
                        co_deltas_mg = deltas_mg,
                        co_deltas_eg = deltas_eg,
                        co_deltas = deltas,
                        co_scores = scores,
                        event = game.event,
                        white_elo = game.white_elo,
                        black_elo = game.black_elo,
                        co_elo = [game.white_elo,
                                  game.black_elo])


def ProcessArgs(db, limit, argv):
    global files

    if argv != "":
        print 'a', argv[0]
        yield StudyGame(db, argv[0])
    else:
        for event in range(1, limit + 1):
            fn = 'generated/game2json/%05d.json' % event
            yield StudyGame(db, fn)
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

def ProcessDeltas(gi, co, deltas):
    dampened_deltas = [min(300, delta) for delta in deltas]
    (delta_median, delta_stddev, delta_avg) = (0, 0, 0)
    if len(dampened_deltas) > 0:
        delta_avg = numpy.mean(dampened_deltas)
        delta_median = numpy.median(dampened_deltas)
        delta_stddev = numpy.std(dampened_deltas)
    return (delta_median, delta_stddev, delta_avg)

def main(argv):
    global game_stages

    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    game_stages = ReadGameStages()

    db = leveldb.LevelDB(FLAGS.analysis, max_open_files=100)

    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)

    for gi_num, gi in enumerate(ProcessArgs(db, FLAGS.limit, argv[1:])):
        if FLAGS.debug:
            print
            print "##### gi_num: ", gi_num, " gi: ", gi
            #print gi.raw_scores[0]
            #print gi.raw_scores[1]            
            print
        for co in [0, 1]:

            (_, _, delta_avg_op) = ProcessDeltas(gi, co, gi.co_deltas_op[co])
            (_, _, delta_avg_mg) = ProcessDeltas(gi, co, gi.co_deltas_mg[co])
            (_, _, delta_avg_eg) = ProcessDeltas(gi, co, gi.co_deltas_eg[co])
            (delta_median, delta_stddev, delta_avg) = ProcessDeltas(gi, co, gi.co_deltas[co])

            standard = {
                '$g_event': gi.event,
                '$g_co_rating': gi.co_elo[co],
                '$g_co': ["w", "b"][co],

                'color_value': [1, -1][co],
                
                'delta_max': safe_max(gi.co_deltas[co]),
                'delta_avg': delta_avg,
                'delta_avg_op': delta_avg_op,
                'delta_avg_mg': delta_avg_mg,
                'delta_avg_eg': delta_avg_eg,

                'delta_avg': delta_avg,
                'delta_avg': delta_avg,
                'delta_median': delta_median,
                'delta_stddev': delta_stddev,
                
                'final_score': gi.final_score,

                'ply_ahead_50': gi.co_ply_ahead_50[co],
                'ply_ahead_100': gi.co_ply_ahead_100[co],
                
                'first_loss_100': gi.first_loss[co][0],
                'first_loss_200': gi.first_loss[co][1],
                'first_loss_300': gi.first_loss[co][2],
            }

            for which in [0, 1, 2, 3, 4]:
                key = 'alt_stages_%d' % which
                if len(gi.alt_stages[co][which]) == 0:
                    standard[key] = 0
                else:
                    standard[key] = numpy.mean([min(300, delta) for delta in gi.alt_stages[co][which]])

            for which in [0, 1, 2, 3, 4]:
                key = 'alt_raw_%d' % which
                key2 = 'alt_raw_stddev_%d' % which 
                slice = gi.raw_scores[co][which * 10 : (which + 1) * 10]
                if len(slice) == 0:
                    standard[key] = 0
                    standard[key2] = 0                    
                else:
                    standard[key] = numpy.mean(slice)
                    standard[key2] = numpy.std(slice) 

            if FLAGS.verbose:
                standard['$g_co_deltas'] = gi.co_deltas[co]
                standard['$g_co_scores'] = gi.co_scores[co]
                
            if FLAGS.key_prefix != '':
                standard2 = {}
                for n, v in standard.iteritems():
                    if n[0] == '$':
                        standard2[n] = v
                    else:
                        standard2[FLAGS.key_prefix + n] = v
                standard = standard2
                
            if FLAGS.debug:
                for n in sorted(standard.keys()):
                    print n, standard[n]
                print
            else:
                print cjson.encode(standard)

if __name__ == '__main__':
    main(sys.argv)



