

passes=2000

for data in b_draw_train.vw b_win_train.vw w_draw_train.vw w_win_train.vw b_lose_train.vw w_lose_train.vw
do 
    (
    base=`basename ${data} .vw`
    rm -f ${base}.cache ${base}.readable ${base}.model ${base}.out ${base}.err ${base}-invert.out$ ${base}-invert.err ${base}.invert
    vw --loss_function=quantile \
        --compressed   \
        --constant=2200  \
        --passes=${passes} \
        --data=${data}  \
        --cache_file=${base}.cache  \
        --readable_model=${base}.readable  \
        --final_regressor=${base}.model > ${base}.out 2> ${base}.err

    vw --passes=1 --invert_hash=${base}.invert --data=${base}.vw >> ${base}-invert.out 2>> ${base}-invert.err
    if [ ! -s ${base}.out ]; then
        rm -f ${base}.out
    fi
    if [ ! -s ${base}-invert.out ]; then
        rm -f ${base}-invert.out
    fi
    printf "%20s | %s\\n" ${data} "`grep 'average loss' ${base}.err`"
    ) &
done

echo waiting
for i in 1 2 3 4 5 6
do
    wait
done

for data in b_draw_train.vw b_win_train.vw w_draw_train.vw w_win_train.vw b_lose_train.vw w_lose_train.vw
do
    base=`basename ${data} .vw`
    xbase=`echo $base | sed -e s/train/test/`
    test=`echo $data | sed -e s/train/test/`
    echo predict $xbase
    vw --data=${test} \
        --testonly \
        --initial_regressor=${base}.model  \
        --predictions=${xbase}.predictions > ${xbase}.shh 2>&1
done