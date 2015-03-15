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

(skip, accept) = (0, 0)

def ProcessFile(db, fn):
    global skip, accept
    ar = os.path.splitext(fn)
    if not os.path.lexists(fn.replace('-res.txt', '-done.txt')):
        print 'Not ready: ', fn
        return
    print 'Process: ', fn        

    for ent in filter(None, file(fn).read().split('\n')):
        try:
            obj = cjson.decode(ent)
            fen = obj['fen']
            try:
                db.Get(ent)
                skip += 1
                continue # already exists
            except KeyError:
                accept += 1
                pass # doesn't exist - continue onward
        
            # Cut down on space a bit.
            del obj['fen']
            del obj['time']
            for an in obj['analysis']:
                del an['time']
            db.Put(fen, cjson.encode(obj))
        except cjson.DecodeError:
            sys.stderr.write('%s: ouch: %s\n' % (fn, ent))
            sys.stderr.flush()
            continue
            #sys.exit(1)


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
    print "Skip  : ", skip
    print "Accept: ", accept    

if __name__ == '__main__':
    main(sys.argv)        
