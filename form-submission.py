#!/usr/bin/python

print 'Event,WhiteElo,BlackElo'

event = 25001
with file('pred.txt') as f:
    row = 0
    white = black = 0
    for line in f.readlines():
        line = line.strip()
        if row % 2 == 0:
            white = float(line)
        else:
            black = float(line)
            print '%d,%.0f,%.0f' % (event, black, white)
            black = white = 0
            event += 1
        row += 1
