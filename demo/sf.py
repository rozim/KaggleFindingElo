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

p = subprocess.Popen('/usr/local/bin/stockfish',
                     stderr=file('stderr.txt', 'w'),
                     stdin=subprocess.PIPE,               
                     stdout=subprocess.PIPE)

print p.stdout.readline()

print 'uci: ', SendCommandAndWaitFor(p, 'uci', 'uciok')
print 'so: ', SendCommand(p, 'setoption name Clear Hash value on')
print 'so: ', SendCommand(p, 'setoption name Hash value 128')
print 'Searching: '

SendCommand(p, 'position fen nbqkbnr/ppp2ppp/8/8/2Bp4/4P3/PP3PPP/RNBQK1NR w KQkq - 0 5')
lines = SendCommandAndWaitFor(p, 'go depth 1', 'bestmove')

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
    
    
    
