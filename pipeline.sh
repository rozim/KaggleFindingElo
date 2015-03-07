

prefix=$1
time ./prepare-model-for-vw.py  --limit=25000 --in_model=model3.xjson --field=${prefix} > ${prefix}.vw


util/holdout --input=${prefix}.vw  --test=${prefix}_test.vw  --train=${prefix}_train.vw  && \
        time sh ./run-vowpal.sh ${prefix}  &&  \
        ./score-predictions.py > score_${prefix}.txt && \
         tail score_${prefix}.txt