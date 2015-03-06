

for ne in 100 1000 2500 5000
do
  for v1 in 1 
  do
    for v2 in 1 
    do
        for v3 in auto sqrt log2
        do
            echo XXX $v1 $v2 $v3 $ne
            time ./random-forest-mega.py --extra --n_estimators=${ne} --limit=25000 --field=game_ply,delta_avg_d2,delta_avg_d3,delta_avg_d13,delta_median_d2,delta_median_d3,delta_median_d13,delta_stddev_d13,delta_max_d2,delta_max_d3,delta_max_d13,first_loss_100_d13,first_loss_200_d13,first_loss_300_d13,first_loss_100_d2,first_loss_200_d2,first_loss_300_d2,first_loss_100_d3,first_loss_200_d3,first_loss_300_d3,i_was_mated,i_played_mate,draw_ply  --min_samples_leaf=$v1 --min_samples_split=$v2 --max_features=$v3
        done
    done
  done
done