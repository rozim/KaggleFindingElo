#!/usr/bin/python
import cjson
import collections
import gflags
import math
import random
import re
import sklearn.ensemble
import sys
import time

FLAGS = gflags.FLAGS

gflags.DEFINE_string('csv', 'submission.csv', '')
gflags.DEFINE_string('field', 'delta_avg_d3,delta_avg_d13,delta_max_d13,delta_median_d13,delta_stddev_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,delta_avg_d13,delta_max_d19,delta_median_d19,delta_stddev_d19,first_loss_100_d19,first_loss_200_d19,first_loss_300_d19,game_ply,i_played_mate,i_was_mated', '')
gflags.DEFINE_integer('limit', 100, '')
gflags.DEFINE_integer('max_depth', -1, '4 may help instead of default')
gflags.DEFINE_integer('n_estimators', 10, '')
gflags.DEFINE_bool('extra', False, '')
gflags.DEFINE_integer('min_samples_leaf', 10, '')
gflags.DEFINE_integer('min_samples_split', 10, '')
gflags.DEFINE_string('max_features', 'auto', '')
gflags.DEFINE_integer('selftest', 1, '')

gflags.DEFINE_string('prefix', '', 'Something like model-d19_')
gflags.DEFINE_string('what', 'b_draw,b_lose,b_win,w_draw,w_lose,w_win', '')

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
                if field != 'final_score':
                    # Ugh, could be negative
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
    train_x = [ent[1] for ent in train]
    train_y = [ent[2] for ent in train]
    ev = [ent[0] for ent in test]
    test_x = [ent[1] for ent in test]
    test_y = [ent[2] for ent in test]

    max_depth = None
    if FLAGS.max_depth > 0:
        max_depth = FLAGS.max_depth
        
    if FLAGS.max_features.find('.') > 0:
        max_features = float(FLAGS.max_features)
    elif re.match("^[0-9]+$", FLAGS.max_features):
        max_features = int(FLAGS.max_features)
    else:
        max_features = FLAGS.max_features
        
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


    return predictions, r.score(train_x, train_y)    

def ParseMaxDepth():
    if FLAGS.max_depth > 0:
        return FLAGS.max_depth
    else:
        return None

def ParseMaxFeatures():    
    if FLAGS.max_features.find('.') > 0:
        return float(FLAGS.max_features)
    elif re.match("^[0-9]+$", FLAGS.max_features):
        return int(FLAGS.max_features)
    else:
        return FLAGS.max_features
    
# Ugh, name is wrong.
def SelfTest(train, pretty):
    random.shuffle(train)
    where = int(len(train) * 0.9) # split point
    train90 = train[0 : where]
    train10 = train[where + 1 : ]
    # tbd: use zip(*)
    train90_x = [ent[1] for ent in train90]
    train90_y = [ent[2] for ent in train90]
    train10_x = [ent[1] for ent in train10]
    train10_y = [ent[2] for ent in train10]    
        
    r = sklearn.ensemble.RandomForestRegressor(n_estimators = FLAGS.n_estimators,
                                               max_features = ParseMaxFeatures(),
                                               max_depth = ParseMaxDepth(),
                                               min_samples_leaf = FLAGS.min_samples_leaf,
                                               min_samples_split = FLAGS.min_samples_split)

    r.fit(train90_x, train90_y)

    deltas = []
    for x, y in zip(train10_x, train10_y):
        predict = r.predict(x)[0]
        deltas.append(abs(predict - y))

    return ((sum(deltas) / len(deltas)),
            r.score(train10_x, train10_y),
            r.score(train90_x, train90_y),
            len(train10_x),
            len(train90_x))

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)
      
    print 'CSV: ', FLAGS.csv
    print 'Field: ', FLAGS.field
    print 'Limit: ', FLAGS.limit
    print 'Depth: ', FLAGS.max_depth
    print 'Estimators: ', FLAGS.n_estimators
    print 'Extra: ', FLAGS.extra
    print 'Min samples leaf: ', FLAGS.min_samples_leaf
    print 'Min samples split: ', FLAGS.min_samples_split
    print 'Max features: ', FLAGS.max_features
    print 'Selftest: ', FLAGS.selftest
    print 'Prefix: ', FLAGS.prefix    
    print 'What: ', FLAGS.what
    print ''

    pretty = MakePretty()
    if FLAGS.selftest > 0:
        cols = []
        for what in FLAGS.what.split(','):
            for i in range(FLAGS.selftest):
                t1 = time.time()
                res, ev10, ev90, eval_size, train_size = SelfTest(ReadAndBreakUp(FLAGS.prefix + what + '_train.xjson'), pretty)
                cols.append((res, ev10, ev90, eval_size))
                print '%10s | %.1f %.4f %.4f | %.1fs (%d %d)' % (what, res, ev10, ev90, time.time() - t1, eval_size, train_size)

        # Properly weigh the score but it seems to always be the same.
        top = bot = 0
        for ent in cols:
            top += abs(ent[0]) * eval_size
            bot += eval_size
        print 'Score: %.4f' % (sum(abs(ent[0]) for ent in cols) / len(cols))            
        print 'Score: %.4f' % (float(top) / bot)
        print 'Ev10:  %.4f' % (sum(abs(ent[1]) for ent in cols) / len(cols))
        print 'Ev90:  %.4f' % (sum(abs(ent[2]) for ent in cols) / len(cols) )       
        sys.exit(0)
        
    w_predictions = {}
    b_predictions = {}
    scores = []
    for what in FLAGS.what.split(','):
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
