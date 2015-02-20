

ls generated/positions/shard_*.txt  | parallel -j+0 --eta  './generate-analysis.py --out=generated/analysis/1/{/.}-res.txt --done=generated/analysis/1/{/.}-done.txt --depth=1 --multipv=5 --engine=/usr/local/bin/stockfish  {} > generated/analysis/1/{/.}.out 2> generated/analysis/1/{/.}.err'