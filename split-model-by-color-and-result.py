#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')

def ProcessModel(f):
    fm_train = {
        'w1.0': file('w_win_train.xjson', 'w'),
        'b1.0': file('b_win_train.xjson', 'w'),
        'w-1.0': file('w_lose_train.xjson', 'w'),
        'b-1.0': file('b_lose_train.xjson', 'w'),
        'w0.0': file('w_draw_train.xjson', 'w'),
        'b0.0': file('b_draw_train.xjson', 'w')
        }
    fm_test = {
        'w1.0': file('w_win_test.xjson', 'w'),
        'b1.0': file('b_win_test.xjson', 'w'),
        'w-1.0': file('w_lose_test.xjson', 'w'),
        'b-1.0': file('b_lose_test.xjson', 'w'),
        'w0.0': file('w_draw_test.xjson', 'w'),
        'b0.0': file('b_draw_test.xjson', 'w')
        }    
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        fm = fm_train
        if row >= 25000:
            fm = fm_test
        obj = cjson.decode(line)
        result = obj['result'] # 1.0, 0.0, -1.0
        co = obj['$g_co'] # w, b        
        key = "%s%.1f" % (co, result)
        fm[key].write(line)
        

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    ProcessModel(file(FLAGS.in_model))

if __name__ == '__main__':
    main(sys.argv)        
