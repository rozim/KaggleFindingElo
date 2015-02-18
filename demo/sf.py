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
            return all
        all.append(line)

def SendCommandAndWaitFor(p, cmd, prefix):
    SendCommand(p, cmd)
    return ReadUntil(p,prefix)

p = subprocess.Popen('/home/dspencer/Stockfish/src/stockfish',
                     stderr=file('stderr.txt', 'w'),
                     stdin=subprocess.PIPE,               
                     stdout=subprocess.PIPE)

print p.stdout.readline()

print 'uci: ', SendCommandAndWaitFor(p, 'uci', 'uciok')
print 'so: ', SendCommand(p, 'setoption name Clear Hash value on')
print 'so: ', SendCommand(p, 'setoption name Hash value 128')
print 'Searching: '
lines = SendCommandAndWaitFor(p, 'go depth 10', 'bestmove')
for line in lines:
    print line
    
    
