
# Performance

Oh man, python-chess is a dog, at least in this test:

time ./read-pgn.py ../data/data-1000.pgn > /dev/null

real	5m0.530s
user	4m30.424s
sys	0m0.164s

Or without a node.board().fen() call

real	3m4.773s
user	2m57.872s
sys	0m0.096s