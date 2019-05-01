#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
        exit
}


for f in $2/*.csv
do
  COURSE=$(echo $f| cut -d'_' -f 2)
  RUN=$(echo $f| cut -d'_' -f 3,4)
  echo "Processing $COURSE $RUN"
  python3 /src/grade_loader.py $1 $COURSE $RUN $f
done