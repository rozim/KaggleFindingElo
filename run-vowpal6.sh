
passes=1000

for data in b_draw_game_ply.vw	b_win_game_ply.vw w_draw_game_ply.vw w_win_game_ply.vw b_lose_game_ply.vw w_lose_game_ply.vw
do
    base=`basename ${data} .vw`
    rm -f ${base}.cache ${base}.readable ${base}.model ${base}.out ${base}.err
    vw --loss_function=quantile \
        --compressed   \
        --constant=2200  \
        --passes=${passes} \
        --data=${data}  \
        --cache_file=${base}.cache  \
        --readable_model=${base}.readable  \
        --final_regressor=${base}.model > ${base}.out 2> ${base}.err
    if [ ! -s ${base}.out ]; then
        rm -f ${base}.out
    fi
    echo ${data} "     " `grep 'average loss' ${base}.err`
done