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

gflags.DEFINE_string('model_dir', '.', '')
gflags.DEFINE_integer('limit', 1000, '')

gflags.DEFINE_bool('debug', False, '')

files = 0

kBoolToInt = {
    True: 1,
    False: 0
    }

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
    is_stalemate = property(lambda me: me._map['is_stalemate'])
    is_mate = property(lambda me: me._map['is_mate'])    


# Static info about a game
GameInfo = namedtuple('GameInfo', ['event',
                                   'white_elo',
                                   'black_elo',
                                   'co_result',
                                   'result',
                                   'co_elo',
                                   'game_ply',
                                   'is_stalemate',
                                   'is_mate',
                                   ])

def StudyGame(fn):
    global game_stages

    with file(fn) as f:

        game = Game(f)

        return GameInfo(game_ply = game.game_ply,
                        is_stalemate = game.is_stalemate,
                        is_mate = game.is_mate,                        
                        event = game.event,
                        white_elo = game.white_elo,
                        black_elo = game.black_elo,
                        result = ParseResult[game.result],
                        co_elo = [game.white_elo,
                                  game.black_elo],
                        co_result = [ParseResult[game.result],
                                     ParseResultFlip[game.result]])


def ProcessArgs(limit, argv):
    global files

    for event in range(1, limit + 1):
        fn = 'generated/game2json/%05d.json' % event
        yield StudyGame(fn)
        files += 1
        if files >= limit:
            break
        
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


def main(argv):
    global game_stages

    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    if len(argv[1:]) == 0:
        print 'Need *.json or (generated/game2json/#####.json) dir (generated/game2json) arg'
        sys.exit(2)

    for gi_num, gi in enumerate(ProcessArgs(FLAGS.limit, argv[1:])):
        (draw_ply, i_played_mate, i_was_mated) = ProcessDrawAndMate(gi)
        for co in [0, 1]:
            standard = {
                '$g_event': gi.event,
                '$g_co_rating': gi.co_elo[co],
                '$g_co': ["w", "b"][co],
                'color_value': [1, -1][co],
                'game_ply': gi.game_ply,
                'result': gi.co_result[co],
                'is_stalemate': kBoolToInt[gi.is_stalemate],
                'i_played_mate': i_played_mate[co],
                'i_was_mated': i_was_mated[co],
            }
            if FLAGS.debug:
                for n in sorted(standard.keys()):
                    print n, standard[n]
                print
            else:
                print cjson.encode(standard)

if __name__ == '__main__':
    main(sys.argv)



