#!/bin/bash

export _REDIS_VER="5.0.5"


if [ -n "$1" ]
then
  	export _REDIS_VER=$1
fi


sed 's/$REDIS_VERSION/'$_REDIS_VER'/' Dockerfile.template > Dockerfile.$_REDIS_VER
echo Building $_REDIS_VER

rm -rf redisu
mkdir redisu
git clone -b main --single-branch https://github.com/redislabs-training/ru101.git redisu
rm -rf redisu/.git
rm -f redisu/.gitignore
rm -f redisu/LICENSE
rm -f redisu/README.md
mv redisu/redisu/ru101 redisu
mv redisu/redisu/utils redisu

docker build -f Dockerfile.$_REDIS_VER -t redisuniversity/ru101-lab .
