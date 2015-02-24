#!/usr/bin/python

# Generate a blacklist of final positions in the test set.
# Very hardcoded.

from chess_util import *
import gflags
import sys
import cjson
import chess_util

FLAGS = gflags.FLAGS
  
def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    out = file('generated/test-blacklist.txt', 'w')
    for event in xrange(25001, 50001):
        fn = 'generated/game2json/%05d.json' % event
        with file(fn, 'r') as f:
            obj = cjson.decode(f.read())
            fen= obj['positions'][-1]['fen']
            simplify = chess_util.SimplifyFen(fen)
            out.write(simplify + '\n')
            if simplify == 'r3r3/1pk3pp/p6q/5p1n/1PP1bP1Q/4b1PP/PB4B1/3R1K1R b - -':
                print event
            
            
if __name__ == '__main__':
    main(sys.argv)
