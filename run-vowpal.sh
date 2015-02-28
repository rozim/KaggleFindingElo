
rm -f *.cache *.readable *.model *.predictions

# TBD: --compressed  

train=delta_avg_train.vw
test=delta_avg_test.vw
passes=200

vw --loss_function=quantile  \
    --compressed \
       --constant=2200 \
        --passes=${passes} \
        --data=${train} \
        --cache_file=latest.cache \
        --readable_model=latest.readable \
        --final_regressor=latest.model

echo "====="

if [ "${test}" ];  then
    vw \
        --data=${test} \
        --testonly \
        --initial_regressor=latest.model \
        --predictions=latest.predictions
fi