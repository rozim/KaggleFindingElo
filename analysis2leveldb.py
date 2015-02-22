#!/usr/bin/python

import cjson
import gflags
import glob
import leveldb
import sys
import os.path

FLAGS = gflags.FLAGS

gflags.DEFINE_string('in_dir', 'generated/analysis/13', 'Input directory, will look for *res.txt')
gflags.DEFINE_string('output', 'd13.leveldb', 'Output file')

def ProcessFile(db, fn):
    ar = os.path.splitext(fn)
    if not os.path.lexists(fn.replace('-res.txt', '-done.txt')):
        print 'Not ready: ', fn
        return
    print 'Process: ', fn        

    for ent in file(fn).read().split('\n'):
        if ent is '':
            continue
        try:
            obj = cjson.decode(ent)
            db.Put(obj['fen'], ent)            
        except cjson.DecodeError:
            print 'ouch: ', ent
            sys.exit(1)


def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)

    db = leveldb.LevelDB(FLAGS.output)

    print 'in: ', FLAGS.in_dir
    for fn in glob.glob(FLAGS.in_dir + '/' + '*res.txt'):
        ProcessFile(db, fn)

if __name__ == '__main__':
    main(sys.argv)        
