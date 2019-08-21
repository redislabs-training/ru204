#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a version number. Example: "
    echo "  ./tag.sh 5"
    exit 1
fi

docker tag redisuniversity/ru102j-lab gcr.io/redis-labs/ru102j-lab:v$1
docker push gcr.io/redis-labs/ru102j-lab:v$1
docker push redisuniversity/ru102j-lab
