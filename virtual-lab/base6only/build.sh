#!/bin/bash

export _ALPINE_VER="3.9"

export _REDIS_VER="6.0.6"
export _REDIS_SHA="12ad49b163af5ef39466e8d2f7d212a58172116e5b441eebecb4e6ca22363d94"
export _REDIS_URL="https://download.redis.io/releases/redis-$_REDIS_VER.tar.gz"

echo Building $_REDIS_VER on $_ALPINE_VER

docker build -t redisuniversity/virtual-lab-base-6only $_BUILD_ARGS \
  --build-arg ALPINE_VERSION=$_ALPINE_VER \
  --build-arg REDIS_VERSION=$_REDIS_VER \
  --build-arg REDIS_DOWNLOAD_SHA=$_REDIS_SHA \
  --build-arg REDIS_DOWNLOAD_URL=$_REDIS_URL .
