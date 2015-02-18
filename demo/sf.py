#!/usr/bin/python

import sys
import subprocess

def SendCommand(p, cmd):
    p.stdin.write(cmd + '\n')

def ReadUntil(p, prefix):
    all = []
    while True:
        line = p.stdout.readline().strip()
        if line.startswith(prefix):
            print "DONE: ", line
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

p = subprocess.Popen('/home/dspencer/Stockfish/src/stockfish',
                     stderr=file('stderr.txt', 'w'),
                     stdin=subprocess.PIPE,               
                     stdout=subprocess.PIPE)

print p.stdout.readline()

print 'uci: ', SendCommandAndWaitFor(p, 'uci', 'uciok')
print 'so: ', SendCommand(p, 'setoption name Clear Hash value on')
print 'so: ', SendCommand(p, 'setoption name Hash value 128')
print 'Searching: '
SendCommand(p, 'position fen 8/p3q2k/1p2p1p1/r2bQ3/3P2R1/8/6P1/5R1K w - - 0 1')
SendCommand(p, 'position fen 2k4r/ppp2p2/2b2B2/7p/6pP/2P1q1bP/PP3N2/R4QK1 b - - 0 1')
SendCommand(p, 'position fen K7/5q2/k7/8/8/8/8/8 w - - 0 1')
lines = SendCommandAndWaitFor(p, 'go depth 10', 'bestmove')



for line in lines:

    ar = line.split()
    if (ar[0] != 'info' or
        ar[1] != 'depth' or
        not 'multipv' in ar or
        not 'score' in ar or
        not 'time' in ar or
        not 'pv' in ar):
        continue
    
    print {'depth' : After(ar, 'depth'),
           'time': int(After(ar, 'time')),
           'nodes': int(After(ar, 'nodes')),
           'score': ParseScore(ar),
           'pv': ar[ar.index('pv') + 1:]}
    
    
    
