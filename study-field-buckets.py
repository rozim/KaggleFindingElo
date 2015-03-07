#!/usr/bin/python

import sys
import cjson
import gflags
import collections
import numpy
import random

FLAGS = gflags.FLAGS
gflags.DEFINE_string('in_model', 'model.xjson', 'Output of generate-model.py')
gflags.DEFINE_string('field', '', '')
gflags.DEFINE_integer('limit', 100, '')

def ProcessModel(f):
    study = collections.defaultdict(list)
    rev_study = collections.defaultdict(list)    
    for row, line in enumerate(f.readlines()):
        if line[0] != '{':
            continue
        if row > FLAGS.limit:
            break

        obj = cjson.decode(line)
        #print row, obj        
        rating = obj['$g_co_rating']
        #print rating
        bucket = (rating / 100) * 100
        #if rating == 2658 and obj[FLAGS.field] < 10:
        #print 'DBG', bucket, '!', obj['$g_event'], "!", obj[FLAGS.field]
        study[bucket].append(obj[FLAGS.field])
        rev_study[int(obj[FLAGS.field])].append(rating)
    return study, rev_study

def Report(study):
    print 'Bucket| #      | Min  | Max  |Median| Mean |  Dev'
    for bucket in sorted(study.keys()):
        ents = study[bucket]
        if len(ents) < 10:
            continue
        random.shuffle(ents)
        sample = ' '.join(["%.0f" % _ for _ in sorted(ents[0:10])])
        print "%4d  | %6d | %4.0f | %4.0f | %4.0f | %4.0f | %4.0f | %s" % (bucket,
                          len(ents),
                          numpy.min(ents),
                          numpy.max(ents),
                          numpy.median(ents),
                          numpy.mean(ents),
                          numpy.std(ents),
                                                                      sample)
                                                                      

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    assert FLAGS.field != ''
    (study, rev_study) = ProcessModel(file(FLAGS.in_model))

    Report(study)
    print
    Report(rev_study)

                          
                          

if __name__ == '__main__':
    main(sys.argv)        
