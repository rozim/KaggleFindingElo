


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