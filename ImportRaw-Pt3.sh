csvout="${1}"/"*.csv"
cat $csvout > allcsv.in
sort -t ";" -k2,2 -u -o allcsv1.csv allcsv.in
cat allcsv1.csv | tr -d "'"  > allcsv.csv
