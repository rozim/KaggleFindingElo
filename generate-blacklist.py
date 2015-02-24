#!/usr/bin/python

# Generate a blacklist of final positions in the test set.
# Very hardcoded.

from chess_util import *
import time
import gflags
import cjson as json
import sys
import os.path
import glob
import cjson

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
            out.write(obj['positions'][-1]['fen'] + '\n')
            
if __name__ == '__main__':
    main(sys.argv)
