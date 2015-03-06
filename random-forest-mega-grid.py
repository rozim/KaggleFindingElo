#!/usr/bin/python

import math
import sys
import cjson
import gflags
import collections
import sklearn.ensemble
import sklearn.grid_search
import random

FLAGS = gflags.FLAGS

gflags.DEFINE_string('field', '', '')
gflags.DEFINE_integer('limit', 100, '')
gflags.DEFINE_integer('n_estimators', 10, '')
gflags.DEFINE_bool('extra', False, '')
gflags.DEFINE_integer('min_samples_leaf', 10, '')
gflags.DEFINE_integer('min_samples_split', 10, '')
gflags.DEFINE_string('max_features', 'auto', '')

def ProcessModel(f):
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        if row >= FLAGS.limit:
            break
        obj = cjson.decode(line)
        ar = FLAGS.field.split(',')
        if FLAGS.extra:
            prelim = [obj[field] for field in ar]
            vec = []
            for ent in prelim:
                vec.append(ent)
                vec.append(ent ** 2)
                vec.append(ent ** 0.5)
                vec.append(math.log(1.0 + ent))
            yield obj['$g_event'], vec, obj['$g_co_rating']                
            pass
        else:
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
    
    r = sklearn.ensemble.RandomForestRegressor()
    #r = sklearn.ensemble.RandomForestRegressor(n_estimators = FLAGS.n_estimators,
    #min_samples_leaf = FLAGS.min_samples_leaf,
    #min_samples_split = FLAGS.min_samples_split,
    #max_features = FLAGS.max_features)    

    #'bootstrap': [True, False],
    #'oob_score': [True, False]    
    grid = sklearn.grid_search.GridSearchCV(r,
                                            {'n_estimators': [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024],
                                             'max_depth': [2, 3],
                                             'max_features': ['auto', 'sqrt', 'log2', 0.9, 0.8, 0.7, 0.6, 0.5],
                                             'min_samples_leaf': [1, 2, 4],
                                             'min_samples_split': [1, 2, 4]},
                                            verbose = 1)
    grid.fit(train_x, train_y)
    print
    print 'grid: ', grid
    print    
    print 'gp: ', grid.get_params()
    print    
    print 'best est: ', grid.best_estimator_
    print    
    print 'best score: ', grid.best_score_
    print
    print 'best params: ', grid.best_params_
    print    
    print 'grid scores: ', grid.grid_scores_
    print    
    
    predictions = {}
    for i, x in enumerate(test_x):
        predictions[ev[i]] = grid.predict(x)
    return predictions, grid.score(train_x, train_y)    

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    w_predictions = {}
    b_predictions = {}
    scores = []
    for what in ['b_draw', 'b_lose', 'b_win', 'w_draw', 'w_lose', 'w_win']:

        (p, score) = Evaluate(ReadAndBreakUp(what + '_train.xjson'),
                              ReadAndBreakUp(what + '_test.xjson'))
        scores.append(score)
        if what[0] == 'w':
            w_predictions = dict(w_predictions.items() + p.items())
        else:
            b_predictions = dict(b_predictions.items() + p.items())
        print 'WHAT: %8s: %.4f' % (what, score)
    print 'Avg: %.4f' % (sum(scores) / float(len(scores)))
    # score to beat: 0.4947 for n=10000 10 10 auto

    f = file('submission-grid.csv', 'w')
    f.write('Event,WhiteElo,BlackElo\n')
    for n in sorted(w_predictions.keys()):
        f.write('%s,%.0f,%.0f\n' % (n, w_predictions[n], b_predictions[n]))
    

if __name__ == '__main__':
    main(sys.argv)        
