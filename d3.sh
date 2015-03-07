d=generated/analysis/3
(cd generated/positions; ls | grep shard_ | sed -e s/shard_// | sed -e s/.txt// ) | while read fn
do
    ./generate-analysis.py --depth=3 --output=${d}/shard_${fn}-res.txt --done=${d}/shard_${fn}-done.txt generated/positions/shard_${fn}.txt
done