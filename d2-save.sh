d=generated/analysis/2
(cd generated/positions; ls | grep shard_ | sed -e s/shard_// | sed -e s/.txt// ) | while read fn
do
    echo ./generate-analysis.py --depth=2 --output=${d}/shard_${fn}-res.txt --done=${d}/shard_${fn}-done.txt generated/positions/shard_${fn}.txt
    exit 1
done