#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
#gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
#gflags.DEFINE_integer('limit', 100, '')

# 2256.972656 b_7551
def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    event2rating = {}
    for line in (_.strip() for _ in file('generated/static.csv')):
        if line[0] =='#':
            continue
        #1,2354,2411,38,1/2-1/2
        (event, white_elo, black_elo, ply, result) = line.split(',')
        event2rating[event] = (int(white_elo), int(black_elo))
    #print event2rating

    f = file('latest.predictions')
    n = 0
    deltas = 0
    for line in (_.strip() for _ in f.readlines()):
        (rating, co_event) = line.split(' ')
        rating = float(rating)
        (co, event) = co_event.split('_')
        assert co in ['w', 'b']
        goal = event2rating[event][{'w':0, 'b':1}[co]]
        deltas += abs(rating - goal)
        stars = ''
        print '%1s | %5s | pred: %4.0f | actual: %4.0f | %4.0f | %s' % (co, event, rating, goal, abs(rating - goal), '*' * int(abs(rating - goal) / 100))
        n += 1
    print
    print '#Deltas: ', deltas
    print '#N     : ', n
    print '#Avg   : %.1f' % (float(deltas) / n)
        

if __name__ == '__main__':
    main(sys.argv)        
