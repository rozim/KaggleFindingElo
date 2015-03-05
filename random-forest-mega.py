#!/usr/bin/python

import math
import sys
import cjson
import gflags
import collections
import sklearn.ensemble
import random

FLAGS = gflags.FLAGS

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
        yield obj['$g_event'], [obj[field] for field in ar], obj['$g_co_rating']

def ReadAndBreakUp(fn):

    all = []
    for ev, x, y in ProcessModel(file(fn)):
        all.append([ev, x, y])
    return all

def Evaluate(train, test):
    train_x = [ent[1] for ent in train]
    train_y = [ent[2] for ent in train]
    ev = [ent[0] for ent in test]
    test_x = [ent[1] for ent in test]
    test_y = [ent[2] for ent in test]
    
    r = sklearn.ensemble.RandomForestRegressor(n_estimators = FLAGS.n_estimators, min_samples_leaf = 10, min_samples_split = 10)

    r.fit(train_x, train_y)
    predictions = {}
    for i, x in enumerate(test_x):
        predictions[ev[i]] = r.predict(x)
    return predictions

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    w_predictions = {}
    b_predictions = {}    
    for what in ['b_draw', 'b_lose', 'b_win', 'w_draw', 'w_lose', 'w_win']:
        print '#', what
        p = Evaluate(ReadAndBreakUp(what + '_train.xjson'),
                     ReadAndBreakUp(what + '_test.xjson'))
        if what[0] == 'w':
            w_predictions = dict(w_predictions.items() + p.items())
        else:
            b_predictions = dict(b_predictions.items() + p.items())            

    f = file('submission.csv', 'w')
    f.write('Event,WhiteElo,BlackElo\n')
    for n in sorted(w_predictions.keys()):
        f.write('%s,%.0f,%.0f\n' % (n, w_predictions[n], b_predictions[n]))
    

if __name__ == '__main__':
    main(sys.argv)        
