#!/bin/bash

export _REDIS_VER="5.0.3"


if [ -n "$1" ]
then
  	export _REDIS_VER=$1
fi


sed 's/$REDIS_VERSION/'$_REDIS_VER'/' Dockerfile.template > Dockerfile.$_REDIS_VER
echo Building $_REDIS_VER

rm -rf src
mkdir src
git clone -b master --single-branch https://github.com/redislabs-training/ru202.git src
rm -rf src/.git

docker build -f Dockerfile.$_REDIS_VER -t redisuniversity/ru202-lab .