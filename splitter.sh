
./split-model-by-color-and-result.py 

field=game_ply
for pre in b_draw b_lose b_win w_draw w_lose w_win
do
    for tt in test train
    do
        echo ${pre}_${tt}
        ./prepare-model-for-vw.py --extra --in_model=${pre}_${tt}.xjson --limit=25000 --field=${field} > ${pre}_${tt}_${field}.vw
    done
done