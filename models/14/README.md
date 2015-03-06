
kitchen sink
added -extra

bash-3.2$ time ./random-forest-mega.py --extra --n_estimators=10000 --limit=25000 --field=game_ply,delta_avg_d2,delta_avg_d3,delta_avg_d13,delta_median_d2,delta_median_d3,delta_median_d13,delta_stddev_d13,delta_max_d2,delta_max_d3,delta_max_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,first_loss_100_d2,first_loss_200_d2,first_loss_300_d2,first_loss_100_d3,first_loss_200_d3,first_loss_300_d3,i_was_mated,i_played_mate,draw_ply 
  b_draw: 0.4832
  b_lose: 0.5052
   b_win: 0.4917
  w_draw: 0.4885
  w_lose: 0.5068
   w_win: 0.4927
Avg: 0.4947

real	358m27.326s
user	357m55.616s
sys	0m17.851s

score 193.13370
marginal improvement 0.00803