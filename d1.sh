
# generated/positions/shard_000000.txt

n=6666
while [ $n -lt 10000 ];
do
    n=`expr $n + 1`
    n6=`printf "%06d" $n`
    ./generate-analysis.py --out=generated/analysis/1/shard_${n6}-res.txt --done=generated/analysis/1/shard_${n6}-done.txt --depth=1 generated/positions/shard_${n6}.txt
done
