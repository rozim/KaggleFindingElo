#!/bin/bash

depth=1

find generated/positions -name 'shard*.txt' | parallel -j+0 --eta "./generate-analysis.py --out=generated/analysis/${depth}/{/.}-res.txt --done=generated/analysis/${depth}/{/.}-done.txt --depth=${depth} --multipv=5 --engine=/usr/local/bin/stockfish  {} > generated/analysis/${depth}/{/.}.out 2> generated/analysis/${depth}/{/.}.err" > nite${depth}.shh 2> nite${depth}.err