#!/usr/bin/python

import collections



all = collections.defaultdict(dict)
for fn in [
    'w_win_test_game_ply.predictions',
    'w_lose_test_game_ply.predictions',
    'w_draw_test_game_ply.predictions',
    'b_win_test_game_ply.predictions',
    'b_lose_test_game_ply.predictions',
    'b_draw_test_game_ply.predictions']:
    for line in file(fn).read().splitlines():
        # 2306.107422 b_25001
        ar = line.split(' ')
        rating = float(ar[0])
        ar2 = ar[1].split('_')
        co = ar2[0]
        event = ar2[1]
        all[int(event)][co] = rating

print 'Event,WhiteElo,BlackElo'        
for event in range(25001, 50001):        
    print '%s,%.0f,%.0f' % (event, all[event]['w'], all[event]['b'])
