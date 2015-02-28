time ./generate-model.py --limit=100 generated/game2json/ && time sh ./latest.sh 2> err


# Fri Feb 27 23:02:17 PST 2015
util/holdout --input=delta_avg.vw  --test=delta_avg_test.vw  --train=delta_avg_train.vw  && \
        time sh ./run-vowpal.sh &&  \
        ./score-predictions.py > score.txt && \
         tail score.txt