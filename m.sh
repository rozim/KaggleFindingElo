
for mem in 32 64 128 256 512 1024
do
    echo $mem
    /usr/bin/time stockfish bench ${mem} 1 19 > shh.${mem} 2>&1
    tail shh.${mem}
    echo " "
done
