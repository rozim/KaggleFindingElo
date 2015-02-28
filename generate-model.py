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

gflags.DEFINE_string('analysis', 'd13.leveldb', ("""Analysis database.
                                                Key = 'simple FEN' """ ))

gflags.DEFINE_string('model_dir', '.', '')
gflags.DEFINE_integer('limit', 1000, '')

(files, hit, miss, n_best_move, n_not_best_move) = (0, 0, 0, 0, 0)

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
                                   'best_count',
                                   'best_pct',
                                   'game_ply',
                                   'white_elo',
                                   'black_elo',
                                   'result',
                                   'is_mate',
                                   'co_elo',
                                   'co_deltas',
                                   'opening',
                                   'co_result',
                                   'first_loss_100',
                                   'first_loss_200',
                                   'first_loss_300'
                                   ])

def StudyGame(db, opening_positions, fn):
    global hit, miss, n_best_move, n_not_best_move
    with file(fn) as f:
        game = Game(f)

        best_count = [0, 0]
        best_try = [0, 0]
        deltas = [[], []]
        first_loss_100 = [0, 0]
        first_loss_200 = [0, 0]
        first_loss_300 = [0, 0]
        opening = set()
        for ply, pos in enumerate(game.positions):
            co = ply % 2
            simple = chess_util.SimplifyFen(pos.fen)

            try:
                raw = db.Get(simple)
                hit += 1
            except KeyError:
                miss += 1
                continue
            simple_pos = simple.split(' ')[0]
            if simple_pos in opening_positions:
                opening.add(simple_pos)
            analysis = GameAnalysis(cjson.decode(raw))
            target_depth = analysis.depth
            move_map = {}
            best_line = None
            for i, line in enumerate(analysis.analysis):
                if line.depth != target_depth:
                    continue
                # First line found at target depth must be the best
                if best_line is None:
                    best_line = line
                move_map[line.pv[0]] = line.score

            best_pv = best_line.pv
            best_move = best_pv[0]
            best_try[co] += 1
            if pos.move == best_move:
                n_best_move += 1
                best_count[co] += 1
            else:
                n_not_best_move += 1
                delta = abs(move_map[best_move] - move_map[pos.move])
                if delta >= 100 and first_loss_100[co] == 0:
                    first_loss_100[co] = ply
                if delta >= 200 and first_loss_200[co] == 0:
                    first_loss_200[co] = ply
                if delta >= 300 and first_loss_300[co] == 0:
                    first_loss_300[co] = ply                    

                if delta == 0:
                    # Regan gives a correction of -0.03 if an equal move was chosen
                    # but which wasn't the 1st rank.
                    deltas[co].append(3)
                else:
                    deltas[co].append(max(3, delta))

        result = ParseResult[game.result]
        best_pct = [0.0, 0.0]
        if best_try[0] > 0:
            best_pct[0] = float(best_count[0]) / best_try[0]
        if best_try[1] > 0:
            best_pct[1] = float(best_count[1]) / best_try[1]
        return GameInfo(game_ply = game.game_ply,
                        first_loss_100 = first_loss_100,
                        first_loss_200 = first_loss_200,
                        first_loss_300 = first_loss_300,
                        opening = opening,
                        co_deltas = deltas,
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




def ProcessArgs(db, opening_positions, limit, argv):
    global files

    for event in range(1, limit + 1):
        fn = 'generated/game2json/%05d.json' % event
        yield StudyGame(db, opening_positions, fn)
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

def ProcessDeltas(gi, co):
    dampened_deltas = [min(300, delta) for delta in gi.co_deltas[co]]
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

    db = leveldb.LevelDB(FLAGS.analysis)

    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)

    opening_positions = ReadOpeningPositions('generated/position-frequency.csv')

    for gi_num, gi in enumerate(ProcessArgs(db, opening_positions, FLAGS.limit, argv[1:])):
        (draw_ply, i_played_mate, i_was_mated) = ProcessDrawAndMate(gi)

        for co in [0, 1]:
            (delta_median, delta_stddev, delta_avg) = ProcessDeltas(gi, co)

            standard = {
                '$g_event': gi.event,                
                '$g_co_rating': gi.co_elo[co],
                '$g_co': ["w", "b"][co],
                '$g_co_deltas': gi.co_deltas[co],
                
                'color_value': [1, -1][co],
                'game_ply': gi.game_ply,
                'result': gi.co_result[co],
                'draw_ply': draw_ply,
                'i_played_mate': i_played_mate[co],
                'i_was_mated': i_was_mated[co],
                'best_count': gi.best_count[co],
                'best_pct': gi.best_pct[co],
                'delta_max': safe_max(gi.co_deltas[co]),
                'delta_avg': delta_avg,
                'delta_median': delta_median,
                'delta_stddev': delta_stddev,
                'first_loss_100': gi.first_loss_100[co],
                'first_loss_200': gi.first_loss_200[co],
                'first_loss_300': gi.first_loss_300[co]
            }
            for pos in gi.opening:
                standard['op_%s' % pos] = 1
            print cjson.encode(standard)


    print
    print "#Hit:            ", hit
    print "#Miss:           ", miss
    print "#Best move:      ", n_best_move
    print "#Not best move:  ", n_not_best_move
    print "#Files:          ", files


if __name__ == '__main__':
    main(sys.argv)

