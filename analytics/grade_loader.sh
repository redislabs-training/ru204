#!/bin/bash


trap ctrl_c INT

function ctrl_c() {
        exit
}

echo "START Loading"
echo `date`

for f in $2/*.csv
do
  COURSE=$(echo $f| cut -d'_' -f 2)
  RUN=$(echo $f| cut -d'_' -f 3,4)
  echo "Processing $COURSE $RUN"
  echo "python grade_loader.py $1 $COURSE $RUN $f"
  python3 grade_loader.py $1 $COURSE $RUN $f
  echo ""
done

echo `date`
echo "END Loading"
