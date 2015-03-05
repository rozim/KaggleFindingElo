

for f in *res.txt
do
  if [ ! -s $f ]; then
    echo $f
  fi
done
