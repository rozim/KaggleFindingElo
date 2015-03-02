

# passes=10000
# b_draw_train_game_ply.vw       average loss = 98.2142 h
# b_win_train_game_ply.vw       average loss = 97.8827 h
# w_draw_train_game_ply.vw       average loss = 100.312 h
# w_win_train_game_ply.vw       average loss = 97.777 h
# b_lose_train_game_ply.vw       average loss = 108.223 h
# w_lose_train_game_ply.vw       average loss = 111.379 h
# 22m

passes=100000

for data in b_draw_train_game_ply.vw b_win_train_game_ply.vw w_draw_train_game_ply.vw w_win_train_game_ply.vw b_lose_train_game_ply.vw w_lose_train_game_ply.vw
do
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
    echo ${data} "     " `grep 'average loss' ${base}.err`

done

echo waiting
for i in 1 2 3 4 5 6
do
    wait
done

for data in b_draw_train_game_ply.vw b_win_train_game_ply.vw w_draw_train_game_ply.vw w_win_train_game_ply.vw b_lose_train_game_ply.vw w_lose_train_game_ply.vw
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