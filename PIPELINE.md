


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
