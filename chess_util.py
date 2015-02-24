#!/usr/bin/python

import sys
import subprocess

# Simplify the FEN string by stripping out the last 2 fields (half move clock and full move #)
# under the assumption that these fields are not signifcant in distinguishing positions when
# we want a set of unique positions.
def SimplifyFen(fen):
    return ' '.join(fen.split()[0:4])


def SendCommand(p, cmd):
    p.stdin.write(cmd + '\n')

def ReadUntil(p, prefix):
    all = []
    while True:
        line = p.stdout.readline().strip()
        if line.startswith(prefix):
            return all
        all.append(line)

def SendCommandAndWaitFor(p, cmd, prefix):
    SendCommand(p, cmd)
    return ReadUntil(p,prefix)

def After(ar, s):
    return ar[ar.index(s) + 1]

def ParseScore(ar):
    i = ar.index('score')
    if ar[i + 1] == 'cp':
        return int(ar[i + 2])
    assert ar[i + 1] == 'mate'
    n = int(ar[i + 2])
    if n > 0:
        return 10000 - n
    else:
        return -10000 - n


def SetFenPosition(p, fen):
    SendCommand(p, 'position fen ' + fen)

def SetOption(p, name, value):
    return SendCommand(p, 'setoption name ' + name + ' value ' + value)
    
def ClearHash(p):
    SetOption(p, 'Clear Hash', 'on')

def StartEngine(exe):    
    p = subprocess.Popen(exe,
                         stdin=subprocess.PIPE,               
                         stdout=subprocess.PIPE)
    SendCommandAndWaitFor(p, 'uci', 'uciok')
    return p

def ParseLine(ar):
    return {'depth' : int(After(ar, 'depth')),
           'time': int(After(ar, 'time')),
           'nodes': int(After(ar, 'nodes')),
           'score': ParseScore(ar),
            'multipv': int(After(ar, 'multipv')),
           'pv': ar[ar.index('pv') + 1:]}

def SearchDepth(p, depth, moves=None):
    ClearHash(p)
    if moves is None:
        cmd = 'go depth %d' % depth
    else:
        cmd = 'go depth %d searchmoves %s' % (depth, moves)
    lines = SendCommandAndWaitFor(p, cmd, 'bestmove')
    nodes = []
    for line in lines:
        #print "LINE: ", line
        ar = line.split()
        if (ar[0] != 'info' or
            ar[1] != 'depth' or
            'upperbound' in ar or
            'lowerbound' in ar or
            not 'multipv' in ar or
            not 'score' in ar or
            not 'time' in ar or
            not 'pv' in ar):
            continue

        nodes.append(ParseLine(ar))
    return nodes

    
