#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide a version number. Example: "
    echo "  ./deploy.sh 5"
    exit 1
fi

docker tag redisuniversity/redisconf-2020 gcr.io/redis-labs/redisconf-2020:v$1
docker push gcr.io/redis-labs/redisconf-2020:v$1
#docker push redisuniversity/redisconf-2020
