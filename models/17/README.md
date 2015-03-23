same cmd as below but n_estimators=10

Your Best Entry ↑
You improved on your best score by 3.93543. 
You just moved up 22 positions on the leaderboard

------------------------------------------------------------


 1749  time ./random-forest-mega.py --extra --prefix=model-d19_ --field=d19_alt_raw_0,d19_alt_raw_1,d19_alt_raw_2,d19_alt_raw_3,d19_alt_raw_4,d19_alt_raw_stddev_0,d19_alt_raw_stddev_1,d19_alt_raw_stddev_2,d19_alt_raw_stddev_3,d19_alt_raw_stddev_4,d19_alt_stages_0,d19_alt_stages_1,d19_alt_stages_2,d19_alt_stages_3,d19_alt_stages_4,d19_complexity,d19_delta_avg,d19_delta_avg_eg,d19_delta_avg_mg,d19_delta_avg_op,d19_delta_max,d19_delta_median,d19_delta_stddev,d19_final_score,d19_first_loss_100,d19_first_loss_200,d19_first_loss_300,d19_pct_best,d19_pct_best2,d19_pct_best3,d19_ply_ahead_100,d19_ply_ahead_50,d19_raw_score_mean,d19_raw_score_median,d19_raw_score_stddev,game_ply,i_was_mated,i_played_mate --n_estimators=100 --limit=25000 --self=0  --csv=model17b.csv

...
   w_win: 0.5546 (49.3s)
Avg: 0.5575


Your Best Entry ↑
Top Ten!
You made the top ten by improving your score by 3.44158. 
You just moved up 10 positions on the leaderboard.

------------------------------------------------------------
n_estimators=1000, score 185.17137, improve by 0.5

Your Best Entry ↑
Top Ten!
You made the top ten by improving your score by 0.50662.


------------------------------------------------------------
./random-forest-mega.py --prefix=model-d19_ --field=d19_alt_raw_0,d19_alt_raw_1,d19_alt_raw_2,d19_alt_raw_3,d19_alt_raw_4,d19_alt_raw_stddev_0,d19_alt_raw_stddev_1,d19_alt_raw_stddev_2,d19_alt_raw_stddev_3,d19_alt_raw_stddev_4,d19_alt_stages_0,d19_alt_stages_1,d19_alt_stages_2,d19_alt_stages_3,d19_alt_stages_4,d19_complexity,d19_delta_avg,d19_delta_avg_eg,d19_delta_avg_mg,d19_delta_avg_op,d19_delta_max,d19_delta_median,d19_delta_stddev,d19_final_score,d19_first_loss_100,d19_first_loss_200,d19_first_loss_300,d19_pct_best,d19_pct_best2,d19_pct_best3,d19_ply_ahead_100,d19_ply_ahead_50,d19_raw_score_mean,d19_raw_score_median,d19_raw_score_stddev,game_ply,i_was_mated,i_played_mate  --limit=25000 --self=0 --grid=10 --csv=model17f.csv > shh7

You made the top ten by improving your score by 0.00381. 
bash-3.2$ grep 'best p' shh7
best params:  {'max_leaf_nodes': 250, 'min_samples_leaf': 20, 'n_estimators': 1000, 'min_samples_split': 64, 'max_features': 0.6, 'max_depth': None}
best params:  {'max_leaf_nodes': 1250, 'min_samples_leaf': 5, 'n_estimators': 1000, 'min_samples_split': 32, 'max_features': 0.5, 'max_depth': None}
best params:  {'max_leaf_nodes': 750, 'min_samples_leaf': 8, 'n_estimators': 1000, 'min_samples_split': 8, 'max_features': 0.8, 'max_depth': None}
best params:  {'max_leaf_nodes': 500, 'min_samples_leaf': 8, 'n_estimators': 1000, 'min_samples_split': 32, 'max_features': 'auto', 'max_depth': None}
best params:  {'max_leaf_nodes': 1500, 'min_samples_leaf': 6, 'n_estimators': 1000, 'min_samples_split': 48, 'max_features': 0.5, 'max_depth': None}
best params:  {'max_leaf_nodes': 750, 'min_samples_leaf': 22, 'n_estimators': 1000, 'min_samples_split': 48, 'max_features': 0.7, 'max_depth': None}

Avg: 0.4652

------------------------------------------------------------
time ./random-forest-mega.py --extra --prefix=model-d19_ --field=d19_alt_raw_0,d19_alt_raw_1,d19_alt_raw_2,d19_alt_raw_3,d19_alt_raw_4,d19_alt_raw_stddev_0,d19_alt_raw_stddev_1,d19_alt_raw_stddev_2,d19_alt_raw_stddev_3,d19_alt_raw_stddev_4,d19_alt_stages_0,d19_alt_stages_1,d19_alt_stages_2,d19_alt_stages_3,d19_alt_stages_4,d19_complexity,d19_delta_avg,d19_delta_avg_eg,d19_delta_avg_mg,d19_delta_avg_op,d19_delta_max,d19_delta_median,d19_delta_stddev,d19_final_score,d19_first_loss_100,d19_first_loss_200,d19_first_loss_300,d19_pct_best,d19_pct_best2,d19_pct_best3,d19_ply_ahead_100,d19_ply_ahead_50,d19_raw_score_mean,d19_raw_score_median,d19_raw_score_stddev,game_ply,i_was_mated,i_played_mate  --limit=25000  --n_estimators=1000  --csv=model17zz.csv --max_features=0.5 --selftest=0 > shh

Avg: 0.4919
Your submission scored 185.27416, which is not an improvement of your best score. Keep trying!

note: may have to stay w/ grid search
------------------------------------------------------------