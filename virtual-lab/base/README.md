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

./build.sh 5.0-rc4

or

./build.sh 5.0-rc5 d070c8a3514e40da5cef9ec26dfd594df0468c203c36398ef2d359a32502b548 https://github.com/antirez/redis/archive/5.0-rc5.tar.gz


## By hand
docker build -t redislabs/virtual-lab:4.0.10 --build-arg REDIS_VERSION=4.0.10 .

# Run
docker run --rm --name redis-lab -p:8888:8888 redislabs/virtual-lab:4.0.10
