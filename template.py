#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
# gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)



if __name__ == '__main__':
    main(sys.argv)
