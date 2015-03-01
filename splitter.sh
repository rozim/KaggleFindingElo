
./split-model-by-color-and-result.py 

field=game_ply
for pre in b_draw b_lose b_win w_draw w_lose w_win
do
    echo $pre
    ./prepare-model-for-vw.py --extra --in_model=${pre}.xjson --limit=25000 --field=${field} > ${pre}_${field}.vw
done