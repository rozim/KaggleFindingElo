#!/usr/bin/python

import cjson
import gflags
import glob
import leveldb
import sys
import os.path
import chess_util

FLAGS = gflags.FLAGS

gflags.DEFINE_string('analysis', 'd13.leveldb', 'Analysis file')

(hit, miss, n_best_move, n_not_best_move) = (0, 0, 0, 0)
xnodes = 0
def ProcessFile(db, fn):
    global hit, miss, n_best_move, n_not_best_move
    global xnodes
    with file(fn) as f:
        # game: ['positions', 'black_elo', 'is_stalemate', 'is_mate', 'result', 'white_elo', 'game_ply', 'event']                
        game = cjson.decode(f.read())
        # pos: ['fen', 'num_legal_moves', 'move', 'san', 'ply']
        for pos in game['positions']:
            # move: d2d3 | san: Qd3
            (fen, move, san) = (pos['fen'], pos['move'], pos['san'])
            simple = chess_util.SimplifyFen(fen)

            try:
                raw = db.Get(simple)
                hit += 1
            except KeyError:
                miss += 1
                continue
            # analysis: ['depth', 'moves', 'analysis'[], 'extra'(opt) ]
            #   analysis in inner list [ ['depth', 'score', 'pv', 'nodes', 'multipv'] ]            
            analysis = cjson.decode(raw)
            target_depth = analysis['depth']
            # ['depth', 'score', 'pv', 'nodes', 'multipv']
            for line in analysis['analysis']:
                if line['depth'] != target_depth:
                    continue
                best_line = line
                break

            best_pv = best_line['pv']
            if best_line['nodes'] > xnodes:
                xnodes = best_line['nodes']
                print xnodes, '!', simple
                print
                print analysis
                print
                
            best_move = best_pv[0]
            if move == best_move:
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
    for fn in sys.argv[1:]:
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
