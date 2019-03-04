# ed-courseware

## Virtual Lab

### Build
./build.sh

or manually

docker build -t redislabs/ru201-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/ru201-lab

### Tag
Need to change <version> to align to AVL version number
docker tag redisuniversity/ru201-lab gcr.io/redis-labs/ru201-lab:<version>

### Push
Push to Docker Hub
docker push redisuniversity/ru201-lab

###Push to GCR for AVL pull
docker push gcr.io/redis-labs/ru201-lab:<version>


## Build zip file
From a running Virtual Lab, run the following

cd /src
zip -r ru201.zip * -x *node_modules* -x redisu/ru201/data/General_Building_Permits.csv
cp ru201.zip /rdb/ru201.zip
