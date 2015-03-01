#!/usr/bin/python

import sys
import cjson
import gflags
import collections
import numpy

FLAGS = gflags.FLAGS
# gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
def Report(header, all):
    print "# ", header
    print 'N      : ', len(all)        
    print 'Min    : ', numpy.min(all)
    print 'Max    : ', numpy.max(all)
    print 'Median :  %.1f' % numpy.median(all)
    print 'Mean   :  %.1f' % numpy.mean(all)
    print 'Dev    :  %.1f' % numpy.std(all)
    print

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    all = []
    all_sum = []
    all_diff = []    
    for line in sys.stdin.read().splitlines():
        ar = line.split(',')
        w = int(ar[0])
        b = int(ar[1])
        result = ar[2]
        all.append(w)
        all.append(b)
        all_sum.append(w + b)
        all_diff.append(w - b)

    Report("All", all)
    Report("All sum", all_sum)
    Report("All diff", all_diff)    
              


if __name__ == '__main__':
    main(sys.argv)
