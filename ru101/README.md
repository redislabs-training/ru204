# ed-courseware

## Virtual Lab

### Build
./build.sh

or manually

docker build -t redislabs/ru101-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/ru101-lab

### Push
Push to Docker Hub
docker push redisuniversity/ru101-lab
