#!/bin/bash

export _REDIS_VER="4.0.10"
export _REDIS_SHA="1db67435a704f8d18aec9b9637b373c34aa233d65b6e174bdac4c1b161f38ca4"
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

docker build -t redislabs/virtual-lab-base:$_REDIS_VER $_BUILD_ARGS --build-arg REDIS_VERSION=$_REDIS_VER --build-arg REDIS_DOWNLOAD_SHA=$_REDIS_SHA --build-arg REDIS_DOWNLOAD_URL=$_REDIS_URL .