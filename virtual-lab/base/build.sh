#!/bin/bash

export _REDIS_VER="5.0.3"
export _REDIS_SHA="e290b4ddf817b26254a74d5d564095b11f9cd20d8f165459efa53eb63cd93e02"
export _REDIS_URL="http://download.redis.io/releases/redis-$_REDIS_VER.tar.gz"


if [ -n "$1" ]
then
  	export _REDIS_VER=$1
	export _REDIS_URL="http://download.redis.io/releases/redis-$_REDIS_VER.tar.gz"
fi
if [ -n "$2" ]
then
 	export _REDIS_SHA=$2
fi
if [ -n "$3" ]
then
 	export _REDIS_URL=$3
fi

echo Building $_REDIS_VER

docker build -t redisuniversity/virtual-lab-base:$_REDIS_VER $_BUILD_ARGS --build-arg REDIS_VERSION=$_REDIS_VER --build-arg REDIS_DOWNLOAD_SHA=$_REDIS_SHA --build-arg REDIS_DOWNLOAD_URL=$_REDIS_URL .
