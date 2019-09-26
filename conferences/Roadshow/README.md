# ed-courseware

## Virtual Lab

### Build
./build.sh

### Run
./run.sh

### Tag
Need to change <version> to align to AVL version number
docker tag redisuniversity/redisconf-streams gcr.io/redis-labs/redisconf-streams:<version>

### Push
Push to Docker Hub
docker push redisuniversity/redisconf-streams

###Push to GCR for AVL pull
docker push gcr.io/redis-labs/redisconf-streams:<version>

