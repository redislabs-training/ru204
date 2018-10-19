# Base Lab Image
This has the following content
- Redis install (default 4.0.10)
- RediSearch
- Nginx
- Orion IDE
- supervirsord
- ttyd

# Builds
The build process will default to 4.0.10, but can be overriden
## Scripted builds
./build.sh


or

./build.sh 5.0-rc4 bfc7a27d3ba990e154e5b56484061f01962d40b7c77b520ed7a940914b267cec
./build.sh 5.0.0 70c98b2d0640b2b73c9d8adb4df63bcb62bad34b788fe46d1634b6cf87dc99a4

or

./build.sh 5.0-rc5 d070c8a3514e40da5cef9ec26dfd594df0468c203c36398ef2d359a32502b548 https://github.com/antirez/redis/archive/5.0-rc5.tar.gz

or


## By hand
docker build -t redislabs/virtual-lab:4.0.10 --build-arg REDIS_VERSION=4.0.10 .

# Run
docker run --rm --name redis-lab -p:8888:8888 redislabs/virtual-lab:4.0.10
