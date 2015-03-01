#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
gflags.DEFINE_string('train', 'generated/data-train-static.csv', '')
gflags.DEFINE_string('test', 'generated/data-test-static.csv', '')

def Predict(ply, result):
    if result == '1-0':
        return (2345, 2221)
    elif result == '0-1':
        return (2202, 2335)
    elif result == '1/2-1/2':
        if ply < 30:
            return (2363, 2384)
        else:
            return (2346, 2357)

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    #Event,WhiteElo,BlackElo,Ply,Result
    #1,2354,2411,38,1/2-1/2

    n = 0
    running = 0
    for line in (file(FLAGS.train).read().splitlines()):
        if line == '' or line[0] == '#':
            continue
        ar = line.split(',')
        w = int(ar[1])
        b = int(ar[2])
        ply = int(ar[3])
        result = ar[4]
        (predict_w, predict_b) = Predict(ply, result)
        running += abs(predict_w - w)
        running += abs(predict_b - b)
        n += 2
    print 'Test score: %.1f' % (running / float(n))

    # Test submission
    f = file('submission.csv','w')
    f.write('Event,WhiteElo,BlackElo\n')
    n = 0
    running = 0
    for line in (file(FLAGS.test).read().splitlines()):
        if line == '' or line[0] == '#':
            continue
        ar = line.split(',')
        ply = int(ar[3])
        result = ar[4]
        (predict_w, predict_b) = Predict(ply, result)
        f.write('%s,%d,%d\n' % (ar[0], predict_w, predict_b))

        

if __name__ == '__main__':
    main(sys.argv)


# Event,WhiteElo,BlackElo
