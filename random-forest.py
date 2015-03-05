#!/usr/bin/python

import math
import sys
import cjson
import gflags
import collections
import sklearn.ensemble
import random

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
gflags.DEFINE_string('field', '', '')
gflags.DEFINE_integer('limit', 100, '')
gflags.DEFINE_integer('n_estimators', 10, '')

def ProcessModel(f):
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        if row >= FLAGS.limit:
            break
        obj = cjson.decode(line)
        ar = FLAGS.field.split(',')
        yield obj['$g_event'], obj['$g_co_rating'], [obj[field] for field in ar]
                                                  

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    all = []
    for y, x in ProcessModel(file(FLAGS.in_model)):
        all.append([x, y])
    random.shuffle(all)
    X = [ent[0] for ent in all]
    Y = [ent[1] for ent in all]


    mark = int(len(X) * 0.9)
    x1 = X[0 : mark]
    y1 = Y[0 : mark]
    x2 = X[mark:]
    y2 = Y[mark:]

    print "mark: ", len(x1), len(x2), len(all)
    
    print "training.."

    r = sklearn.ensemble.RandomForestRegressor(n_estimators = FLAGS.n_estimators, min_samples_leaf = 10, min_samples_split = 10)
    r.fit(x1, y1)

    print "trained: ", r.oob_score
    diff = 0
    n = 0
    for x, y in zip(x2, y2):
        n += 1
        this_diff = abs(y - r.predict(x)[0])
        diff += this_diff
        #print x, y, r.predict(x)[0], this_diff
    print "n=", n, " avg=", (diff/n)
    print r.get_params()
    print r
    

if __name__ == '__main__':
    main(sys.argv)        
