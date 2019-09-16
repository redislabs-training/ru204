#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a version number. Example: "
    echo "  ./deploy.sh 5"
    exit 1
fi

docker tag redisuniversity/roadshow gcr.io/redis-labs/roadshow:v$1
docker push gcr.io/redis-labs/roadshow:v$1
# docker push redisuniversity/roadshow-lab
