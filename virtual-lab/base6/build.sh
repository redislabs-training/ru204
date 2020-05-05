#!/bin/bash

export _ALPINE_VER="3.7"
export _REDIS_5_VER="5.0.8"
export _REDIS_5_SHA="f3c7eac42f433326a8d981b50dba0169fdfaf46abb23fcda2f933a7552ee4ed7"
export _REDIS_5_URL="http://download.redis.io/releases/redis-$_REDIS_5_VER.tar.gz"

export _REDIS_6_VER="6.0.1"
export _REDIS_6_SHA="b8756e430479edc162ba9c44dc89ac394316cd482f2dc6b91bcd5fe12593f273"
export _REDIS_6_URL="http://download.redis.io/releases/redis-$_REDIS_6_VER.tar.gz"

echo Building $_REDIS_5_VER and $_REDIS_6_VER on $_ALPINE_VER

docker build -t redisuniversity/virtual-lab-base-6 $_BUILD_ARGS \
  --build-arg ALPINE_VERSION=$_ALPINE_VER \
  --build-arg REDIS_5_VERSION=$_REDIS_5_VER \
  --build-arg REDIS_5_DOWNLOAD_SHA=$_REDIS_5_SHA \
  --build-arg REDIS_5_DOWNLOAD_URL=$_REDIS_5_URL \
  --build-arg REDIS_6_VERSION=$_REDIS_6_VER \
  --build-arg REDIS_6_DOWNLOAD_SHA=$_REDIS_6_SHA \
  --build-arg REDIS_6_DOWNLOAD_URL=$_REDIS_6_URL .
