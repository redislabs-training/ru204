# Base Lab Image
This has the following content
- Redis install (default 4.0.10)
- RediSearch
- Nginx
- supervirsord
- ttyd

# Builds
The build process will default to 4.0.10, but can be overriden
## Scripted builds
./build.sh


or

./build.sh 5.0-rc4 bfc7a27d3ba990e154e5b56484061f01962d40b7c77b520ed7a940914b267cec
./build.sh 5.0.3 e290b4ddf817b26254a74d5d564095b11f9cd20d8f165459efa53eb63cd93e02

or

./build.sh 5.0-rc5 d070c8a3514e40da5cef9ec26dfd594df0468c203c36398ef2d359a32502b548 https://github.com/antirez/redis/archive/5.0-rc5.tar.gz

or


## By hand
docker build -t redisuniversity/virtual-lab-base:4.0.10 --build-arg REDIS_VERSION=4.0.10 .

# Run
docker run --rm --name redis-lab -p:8888:8888 redisuniversity/virtual-lab-base:4.0.10
