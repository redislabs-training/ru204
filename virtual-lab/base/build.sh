#!/bin/bash

export _ALPINE_VER="3.7"
export _REDIS_VER="5.0.5"
export _REDIS_SHA="2139009799d21d8ff94fc40b7f36ac46699b9e1254086299f8d3b223ca54a375"
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

echo Building $_REDIS_VER on $_ALPINE_VER

docker build -t redisuniversity/virtual-lab-base:$_REDIS_VER $_BUILD_ARGS \
  --build-arg ALPINE_VERSION=$_ALPINE_VER \
  --build-arg REDIS_VERSION=$_REDIS_VER \
  --build-arg REDIS_DOWNLOAD_SHA=$_REDIS_SHA \
  --build-arg REDIS_DOWNLOAD_URL=$_REDIS_URL .
