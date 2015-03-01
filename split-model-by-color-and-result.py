#!/usr/bin/python

import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')

def ProcessModel(f):
    fm = {
        'w1.0': file('w_win.xjson', 'w'),
        'b1.0': file('b_win.xjson', 'w'),
        'w-1.0': file('w_lose.xjson', 'w'),
        'b-1.0': file('b_lose.xjson', 'w'),
        'w0.0': file('w_draw.xjson', 'w'),
        'b0.0': file('b_draw.xjson', 'w')
        }
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        if row >= 25000:
            break
        obj = cjson.decode(line)
        #print row, obj        
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
