


# Fri Feb 27 23:02:17 PST 2015
Sat Feb 28 08:58:36 PST 2015

# rebuild xjson
time ./generate-model.py --limit=25000 generated/game2json/ > model9.xjson

# extract 1 field
time ./prepare-model-for-vw.py  --limit=25000 --field=delta_max > delta_max.vw

# study correlation of 1 field /w regression
util/holdout --input=delta_avg.vw  --test=delta_avg_test.vw  --train=delta_avg_train.vw  && \
        time sh ./run-vowpal.sh &&  \
        ./score-predictions.py > score.txt && \
         tail score.txt

# study field bucketization
./study-field-buckets.py --field=delta_avg_d13  --in_model=w_lose.xjson --limit=25000

Sat Feb 28 21:14:01 PST 2015

time ./study-headers.py < generated/twic-blacklist-filtered-headers.csv > generated/twic-blacklist-filtered-headers-report.txt

Sun Mar  1 13:50:36 PST 2015

# 0
./generate-model.py


# 1a.
#   in  = model.xjson
#   out = {w,b}_{win,lose,draw}.xjson
# 1b. 
#   in = {w,b}_{win,lose,draw}.xjson
#   out= {w,b}_{win,lose,draw}.vw
./splitter.sh

# 2
#   in =  {w,b}_{win,lose,draw}.vw
#   out = {w,b}_{win,lose,draw}.{err,model,readable}
./run-vowpal6.sh 

#
# Sun Mar  1 14:31:58 PST 2015

 ./generate-model.py --limit=50000 generated/game2json/ > model5.xjson
./splitter.sh
./run-vowpal6.sh 
./form-submission6.py > models/9/submission9.csv

# Thu Mar  5 00:05:07 PST 2015
# random forest
time ./random-forest-mega.py --n_estimators=500 --limit=25000 --field=game_ply,delta_avg_d2,delta_avg_d3,delta_avg_d13,delta_median_d2,delta_median_d3,delta_median_d13,delta_stddev_d2,delta_stddev_d3,delta_stddev_d13,delta_max_d2,delta_max_d3,delta_max_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,first_loss_100_d2,first_loss_200_d2,first_loss_300_d2,first_loss_100_d3,first_loss_200_d3,first_loss_300_d3,i_was_mated,i_played_mate,draw_ply 

Fri Mar  6 08:46:16 PST 2015

                 nice time ./random-forest-mega-grid.py --extra --limit=25000 --field=game_ply,delta_avg_d2,delta_avg_d3,delta_avg_d13,delta_median_d2,delta_median_d3,delta_median_d13,delta_stddev_d13,delta_max_d2,delta_max_d3,delta_max_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,first_loss_100_d2,first_loss_200_d2,first_loss_300_d2,first_loss_100_d3,first_loss_200_d3,first_loss_300_d3,i_was_mated,i_played_mate,draw_ply --min_samples_leaf=10 --min_samples_split=5 --max_features=auto >&rfg.shh

Sun Mar  8 23:18:43 PDT 2015

time ./random-forest-mega.py --extra --field=delta_avg_d3,delta_avg_d13,delta_max_d13,delta_median_d13,delta_stddev_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,delta_avg_d13,delta_max_d19,delta_median_d19,delta_stddev_d19,first_loss_100_d19,first_loss_200_d19,first_loss_300_d19,game_ply,i_played_mate,i_was_mated  --n_estimators=5000 --limit=25000  --csv=s5k.csv > rf.out 2> rf.err &

Wed Mar 18 17:55:39 PDT 2015

nohup nice time ./generate-model-from-analysis.py --analysis=d19.leveldb --limit=50000 generated/game2json/ > model-d19b.xjson 
nohup nice time ./generate-model-static.py --limit=50000 generated/game2json/ > model-static.xjson 

time ./random-forest-mega.py --extra --prefix=model-d19_ --field=first_loss_300,first_loss_200,first_loss_100 --n_estimators=10 --limit=10000 --self=10  --csv=foo.csv
./split-model-by-color-and-result.py  --in_model=model-d13.xjson


# add key prefix and --verbose defaults to false
./generate-model-from-analysis.py --analysis=d13.leveldb --limit=50000 --key_prefix=d13_ generated/game2json/ > model-d13c.xjson


# no dir arg
./generate-model-from-analysis.py --analysis=d19.leveldb --limit=50000  --key_prefix=d19_  > model-d19.xjson 

./split-model-by-color-and-result.py  --in_model=model-d13.xjson
./split-model-by-color-and-result.py  --in_model=model-d19.xjson

Schema
$g_co
$g_co_rating
$g_event
color_value
result

d19_alt_raw_0
d19_alt_raw_1
d19_alt_raw_2
d19_alt_raw_3
d19_alt_raw_4
d19_alt_raw_stddev_0
d19_alt_raw_stddev_1
d19_alt_raw_stddev_2
d19_alt_raw_stddev_3
d19_alt_raw_stddev_4
d19_alt_stages_0
d19_alt_stages_1
d19_alt_stages_2
d19_alt_stages_3
d19_alt_stages_4
d19_complexity
d19_delta_avg
d19_delta_avg_eg
d19_delta_avg_mg
d19_delta_avg_op
d19_delta_max
d19_delta_median
d19_delta_stddev
d19_final_score
d19_first_loss_100
d19_first_loss_200
d19_first_loss_300
d19_pct_best
d19_pct_best2
d19_pct_best3
d19_ply_ahead_100
d19_ply_ahead_50
d19_raw_score_mean
d19_raw_score_median
d19_raw_score_stddev

Methodology
DONE - get some submission in at least as a sanity check
- random grid search
- better submission
- later try to fold in d7m5

time ./random-forest-mega.py --prefix=model-d19_ --field=d19_alt_raw_0,d19_alt_raw_1,d19_alt_raw_2,d19_alt_raw_3,d19_alt_raw_4,d19_alt_raw_stddev_0,d19_alt_raw_stddev_1,d19_alt_raw_stddev_2,d19_alt_raw_stddev_3,d19_alt_raw_stddev_4,d19_alt_stages_0,d19_alt_stages_1,d19_alt_stages_2,d19_alt_stages_3,d19_alt_stages_4,d19_complexity,d19_delta_avg,d19_delta_avg_eg,d19_delta_avg_mg,d19_delta_avg_op,d19_delta_max,d19_delta_median,d19_delta_stddev,d19_final_score,d19_first_loss_100,d19_first_loss_200,d19_first_loss_300,d19_pct_best,d19_pct_best2,d19_pct_best3,d19_ply_ahead_100,d19_ply_ahead_50,d19_raw_score_mean,d19_raw_score_median,d19_raw_score_stddev,game_ply,i_was_mated,i_played_mate  --limit=25000 --self=0 --grid=100 --csv=model17d.csv > shh5