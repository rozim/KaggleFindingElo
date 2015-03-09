#!/usr/bin/python
import numpy
import math
import sys
import cjson
import gflags
import collections
import sklearn.ensemble
import random
import time

FLAGS = gflags.FLAGS

gflags.DEFINE_string('csv', 'submission.csv', '')
gflags.DEFINE_string('field', '', '')
gflags.DEFINE_integer('limit', 100, '')
gflags.DEFINE_integer('max_depth', -1, '')
gflags.DEFINE_integer('n_estimators', 10, '')
gflags.DEFINE_bool('extra', False, '')
gflags.DEFINE_integer('min_samples_leaf', 10, '')
gflags.DEFINE_integer('min_samples_split', 10, '')
gflags.DEFINE_string('max_features', 'auto', '')

def MakePretty():
    vec = []
    for ent in FLAGS.field.split(','):
        vec.append(ent)
        vec.append(ent + '_sq')
        vec.append(ent + '_sqrt')
        vec.append(ent + '_log')
    return vec

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

def Evaluate(train, test, pretty):
    train = numpy.array(train)
    
    
    train_x = [ent[1] for ent in train]
    train_y = [ent[2] for ent in train]
    ev = [ent[0] for ent in test]
    test_x = [ent[1] for ent in test]
    test_y = [ent[2] for ent in test]

    max_depth = None
    if FLAGS.max_depth > 0:
        max_depth = FLAGS.max_depth
    if FLAGS.max_features.find('.'):
        max_features = float(FLAGS.max_features)
    elif re.match("^[0-9]+$", FLAGS.max_features):
        max_features = int(FLAGS.max_features)
    else:
        max_features = FLAGS.max_feature
    r = sklearn.ensemble.RandomForestRegressor(n_estimators = FLAGS.n_estimators,
                                               max_features = max_features,
                                               max_depth = max_depth,
                                               min_samples_leaf = FLAGS.min_samples_leaf,
                                               min_samples_split = FLAGS.min_samples_split)

    r.fit(train_x, train_y)
    
    predictions = {}
    for i, x in enumerate(test_x):
        predictions[ev[i]] = r.predict(x)

    ar = []
    for p, v in zip(pretty, r.feature_importances_):
        ar.append((v, p))

    for ent in sorted(ar):
        if ent[0] > 0.0:
            print "%.4f : %s" % (ent[0], ent[1])
    print
    print 'OOB: ', r.oob_score

    return predictions, r.score(train_x, train_y)    

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    pretty = MakePretty()
    w_predictions = {}
    b_predictions = {}
    scores = []
    for what in ['b_draw', 'b_lose', 'b_win', 'w_draw', 'w_lose', 'w_win']:
        t1 = time.time()
        (p, score) = Evaluate(ReadAndBreakUp(what + '_train.xjson'),
                              ReadAndBreakUp(what + '_test.xjson'),
                              pretty)
        scores.append(score)
        if what[0] == 'w':
            w_predictions = dict(w_predictions.items() + p.items())
        else:
            b_predictions = dict(b_predictions.items() + p.items())
        print '%8s: %.4f (%.1fs)' % (what, score, time.time() - t1)
    print 'Avg: %.4f' % (sum(scores) / float(len(scores)))
    # score to beat: 0.4947 for n=10000 10 10 auto

    f = file(FLAGS.csv, 'w')
    f.write('Event,WhiteElo,BlackElo\n')
    for n in sorted(w_predictions.keys()):
        f.write('%s,%.0f,%.0f\n' % (n, w_predictions[n], b_predictions[n]))
    

if __name__ == '__main__':
    main(sys.argv)        
