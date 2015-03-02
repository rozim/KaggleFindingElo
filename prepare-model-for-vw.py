#!/usr/bin/python

import math
import sys
import cjson
import gflags
import collections

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
gflags.DEFINE_string('field', '', '')
gflags.DEFINE_integer('limit', 100, '')
gflags.DEFINE_bool('extra', False, '')


def ProcessModel(f):
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        if row > FLAGS.limit:
            break
        obj = cjson.decode(line)
        if FLAGS.extra:

            #field = FLAGS.field
            emit = "%4d '%s_%s|" % (
                obj['$g_co_rating'],
                obj['$g_co'],
                obj['$g_event'])
            ar = FLAGS.field.split(',')
            for field in ar:
                val = obj[field]
                    
                chunk = " %s:%.6f %s:%.6f %s:%.6f %s:%.6f" % (
                    field, val,
                    field + '_pow2', val ** 2,
                    field + '_sqrt' , val ** 0.5,
                    field + '_log', math.log(1 + val))
                emit += chunk
            print emit
        else:
            ar = FLAGS.field.split(',')
            emit = "%4d '%s_%s|" % (obj['$g_co_rating'], obj['$g_co'], obj['$g_event'])
            for field in ar:
                val = obj[field]
                val = obj[field]
                chunk =  " %s:%.6f" % (field, val)
                emit += chunk
            print emit
                                                  

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    ProcessModel(file(FLAGS.in_model))

if __name__ == '__main__':
    main(sys.argv)        
