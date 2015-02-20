#!/usr/bin/python

from chess_util import *
import time
import gflags
  
FLAGS = gflags.FLAGS
  
gflags.DEFINE_integer('depth', 1, 'Depth to search')
gflags.DEFINE_integer('hash', 128, 'Hash table size')
gflags.DEFINE_integer('multipv', 1, 'Moves to search')
gflags.DEFINE_string('engine', '/home/dspencer/Stockfish/src/stockfish', '')

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    p = StartEngine(FLAGS.engine)

    SetOption(p, 'Hash', '%d' % FLAGS.hash)
    if FLAGS.multipv > 1:
        SetOption(p, 'MultiPV', '%d' % FLAGS.multipv)

    positions = 0
    t1 = time.time()
    for fn in argv[1:]:
        print 'OPEN', fn
        with file(fn) as f:
            for line in f.readlines():
                (fen,moves) = line.split(',')
                SetFenPosition(p, fen)
                # {'pv': ['f7f5', 'e4f5'], 'depth': '2', 'score': -32, 'time': 2, 'nodes': 223, 'multipv': 1}
                positions += 1
                for depth_report in SearchDepth(p, FLAGS.depth):
                    print depth_report
                print
                if positions % 100 == 0:
                    print "%d. %.1f" % (positions, time.time() - t1)
                if positions > 10000:
                    break    

if __name__ == '__main__':
    main(sys.argv)
