
rm -f *.cache *.readable *.model *.predictions

# TBD: --compressed  

prefix=$1
train=${prefix}_train.vw
test=${prefix}_test.vw
passes=250

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