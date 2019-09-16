# ed-courseware

## Virtual Lab

### Build
./build.sh

or manually

docker build -t redisuniversity/redisconf-basicredis .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-basicredis

### Tag
Need to change <version> to align to AVL version number
docker tag redisuniversity/redisconf-basicredis gcr.io/redis-labs/redisconf-basicredis:<version>

### Push
Push to Docker Hub
docker push redisuniversity/redisconf-basicredis

###Push to GCR for AVL pull
docker push gcr.io/redis-labs/redisconf-basicredis:<version>


## Build zip file
From a running Virtual Lab, run the following
