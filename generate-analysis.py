#!/usr/bin/python

from chess_util import *

import gflags
import os.path
import sys
import time

try:
    import cjson
    def encode(obj):
      return cjson.encode(obj)
    def decode(obj):
      return cjson.decode(obj)    
except ImportError:
  import json
  def encode(obj):
    return json.dumps(obj)
  def decode(obj):
    return json.loads(obj)  
  


FLAGS = gflags.FLAGS
  
gflags.DEFINE_integer('depth', 1, 'Depth to search')
gflags.DEFINE_integer('hash', 128, 'Hash table size')
gflags.DEFINE_integer('multipv', 1, 'Moves to search')
gflags.DEFINE_string('output', '', 'Output file')
gflags.DEFINE_string('done', '', 'Done file')
gflags.DEFINE_string('engine', '/usr/local/bin/stockfish', '')

def Analyze(p, fen, moves):
    t1 = time.time()
    SetFenPosition(p, fen)
    # {'pv': ['f7f5', 'e4f5'], 'depth': '2', 'score': -32, 'time': 2, 'nodes': 223, 'multipv': 1}
    best_moves = set()
    res = []
    for depth_report in SearchDepth(p, FLAGS.depth):
        res.append(depth_report)
        if depth_report['depth'] == FLAGS.depth:
            best_moves.add(depth_report['pv'][0])
    analysis = {'fen': fen,
                'depth': FLAGS.depth,
                'moves': moves,
                'analysis': res}            
    for move in moves:
        extra = []
        if move not in best_moves:
            extra.append(move)
            for depth_report in SearchDepth(p, FLAGS.depth, move):
                res.append(depth_report)
        if len(extra) > 0:
            analysis['extra'] = extra
    analysis['time'] = '%.1f' % (time.time() - t1)
    return analysis


def AnalyzeFromLine(p, line):
    (fen,moves) = line.split(',')
    return Analyze(p, fen, moves.split(':'))

def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)
      
    if FLAGS.output == '':
        print 'Need --output'
        sys.exit(2)

    if FLAGS.done != '' and os.path.isfile(FLAGS.done):
        print 'Already done'
        sys.exit(0)
        
    p = StartEngine(FLAGS.engine)

    SetOption(p, 'Hash', '%d' % FLAGS.hash)
    if FLAGS.multipv > 1:
        SetOption(p, 'MultiPV', '%d' % FLAGS.multipv)

    positions = 0
    t1 = time.time()
    out = file(FLAGS.output, 'w')
    for fn in argv[1:]:
        print 'OPEN', fn
        with file(fn) as f:
            for line in f.readlines():
                res = AnalyzeFromLine(p, line.strip())
                out.write(encode(res))
                out.write('\n\n')
                positions += 1
                if positions % 100 == 0:
                    print "%d. %.1f" % (positions, time.time() - t1)
                    sys.stdout.flush()
                    out.flush()

    if FLAGS.done != '':
        with file(FLAGS.done, 'w') as fdone:
            fdone.write(time.ctime())

if __name__ == '__main__':
    main(sys.argv)
