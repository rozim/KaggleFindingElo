
passes=10

for data in b_draw_game_ply.vw	b_win_game_ply.vw w_draw_game_ply.vw w_win_game_ply.vw b_lose_game_ply.vw w_lose_game_ply.vw
do
    base=`basename ${data} .vw`
    (
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
    echo ${data} "     " `grep 'average loss' ${base}.err`
    ) &
done

echo waiting
for i in 1 2 3 4 5 6
do
    wait
done