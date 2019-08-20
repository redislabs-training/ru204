# Base IDE Lab Image
This has the following content
- Redis install (default 4.0.10)
- RediSearch
- Nginx
- supervirsord
- ttyd

# Build
./build.sh

or manually...

docker build -f Dockerfile.5.0.3 -t redisuniversity/virtual-lab-ide:5.0.3 .

# Run
docker run --rm --name redis-lab -p:8888:8888 redisuniversity/virtual-lab-ide:5.0.3