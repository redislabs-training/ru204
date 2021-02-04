# ed-courseware

## Virtual Lab

### Build
./build.sh

or manually

docker build -t redislabs/ru202-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/ru202-lab

### Push
Push to Docker Hub
docker push redisuniversity/ru202-lab

## Build zip file
From a running Virtual Lab, run the following

zip -r ru202.zip *
