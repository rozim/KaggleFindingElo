
rm -f *.buffer dump.nice.txt dump.raw.txt *.model pred.txt 

xgboost=/usr/local/bin/xgboost
model=latest.model

rm -f ${model}

echo "====="
echo Building
${xgboost}  xg.conf 
echo "====="
echo Predicting
${xgboost}  xg.conf task=pred model_in=${model}
echo "====="
${xgboost}  xg.conf task=dump model_in=${model} name_dump=dump.raw.txt
echo "====="
${xgboost}  xg.conf task=dump model_in=${model} fmap=featmap.txt name_dump=dump.nice.txt 
echo "====="
python xg-score.py latest-test.svm
