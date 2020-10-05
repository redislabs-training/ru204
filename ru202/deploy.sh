#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a version number. Example: "
    echo "  ./deploy.sh 5"
    exit 1
fi

docker tag redisuniversity/ru202-lab gcr.io/redis-labs/ru202-lab:v$1
docker push gcr.io/redis-labs/ru202-lab:v$1
docker push redisuniversity/ru202-lab