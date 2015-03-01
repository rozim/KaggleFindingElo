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
    all_w_wwin = []
    all_b_wwin = []
    all_w_bwin = []
    all_b_bwin = []
    all_w_draw = []
    all_b_draw = []
    all_w_gm_draw = []
    all_b_gm_draw = []
    all_w_draw_length = collections.defaultdict(list)
    all_b_draw_length = collections.defaultdict(list)
    for line in sys.stdin.read().splitlines():
        ar = line.split(',')
        w = int(ar[0])
        b = int(ar[1])
        result = ar[2]
        ply = int(ar[3])
        all.append(w)
        all.append(b)
        all_sum.append(w + b)
        all_diff.append(w - b)

        if result == '1-0':
            all_w_wwin.append(w)
            all_b_wwin.append(b)
        elif result == '0-1':
            all_w_bwin.append(w)
            all_b_bwin.append(b)
        elif result == '1/2-1/2':
            all_w_draw.append(w)
            all_b_draw.append(b)
            all_w_draw_length[(ply / 10) * 10].append(w)
            all_b_draw_length[(ply / 10) * 10].append(b) 
            if ply < 30:
                all_w_gm_draw.append(w)
                all_b_gm_draw.append(b)                

    Report("All", all)
    Report("All sum", all_sum)
    Report("All diff", all_diff)

    Report("W, White Wins", all_w_wwin)
    Report("B, White Wins", all_b_wwin)
    Report("W, Black Wins", all_w_bwin)
    Report("B, Black Wins", all_b_bwin)
    Report("W, Draw", all_w_draw)
    Report("B, Draw", all_b_draw)
    Report("W, GM Draw", all_w_gm_draw)
    Report("B, GM Draw", all_b_gm_draw)


    w_vector = []
    b_vector = []    
    for length in sorted(all_w_draw_length.keys()):
        if len(all_w_draw_length[length]) + len(all_b_draw_length[length]) < 100:
            continue
        Report("W, GM Draw length %d" % length, all_w_draw_length[length])
        Report("B, GM Draw length %d" % length, all_b_draw_length[length])

        w_vector.append((length, numpy.mean(all_w_draw_length[length])))
        b_vector.append((length, numpy.mean(all_b_draw_length[length])))

    print
    print 'White,Black mean rating by draw length'
    for i, ent in enumerate(w_vector):
        print "%d %.0f %.0f" % (ent[0], ent[1], b_vector[i][1])
    
      
        

if __name__ == '__main__':
    main(sys.argv)
