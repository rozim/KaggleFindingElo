cat generated/positions/shard-list.txt  | util/shuffle | parallel -j+0 --eta  './generate-analysis.py --out=generated/analysis/19/{/.}-res.txt --done=generated/analysis/19/{/.}-done.txt --depth=19 --engine=/usr/local/bin/stockfish  {} > generated/analysis/19/{/.}.out 2> generated/analysis/19/{/.}.err' >& d19.shh