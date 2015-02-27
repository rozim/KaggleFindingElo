
rm -f *.cache *.readable *.model *.predictions

# TBD: --compressed  

vw --loss_function=quantile  \
`       --constant=2200 \
        --passes=1000 \
        --data=latest-train.vw \
        --cache_file=latest-train.cache \
        --readable_model=latest-train.readable \
        -f latest-train.model

echo "====="

vw --cache_file=latest-train.cache \
        --data=latest-test.vw \
        --testonly \
        --initial_regressor=latest-train.model \
        --predictions=latest-test.predictions