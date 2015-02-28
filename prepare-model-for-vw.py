#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
gflags.DEFINE_integer('limit', 100, '')

def ProcessModel(f):
    global FLAGS
    row = 0
    #master = collections.defaultdict(set)
    for line in f.readlines():
        if line[0] != '{':
            continue
        row += 1
        if row > FLAGS.limit:
            break
        obj = cjson.decode(line)
        print "%4d '%s_%s| delta_avg:%.1f" % (obj['$g_co_rating'], obj['$g_co'], obj['$g_event'], obj['delta_avg']) 
        #for n, v in obj.iteritems():
            #if n[0:3] == 'op_':
            #continue
            #master[n].add(str(v))
        # ['$g_co', '$g_co_deltas', '$g_co_rating', '$g_event', 'best_pct', 'best_count', 'color_value', 'delta_avg', 'delta_max', 'delta_median', 'delta_stddev', 'draw_ply', 'first_loss_100', 'first_loss_200', 'first_loss_300', 'game_ply', 'i_played_mate', 'i_was_mated', 'op_rnbq1rk1/pp1pppbp/5np1/2p5/2P5/1P2PN2/PB1PBPPP/RN1QK2R', 'result']        



    #for n, v in master.iteritems():
    #print n, len(v)
                                                  

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    ProcessModel(file(FLAGS.in_model))

if __name__ == '__main__':
    main(sys.argv)        
