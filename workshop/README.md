# ed-courseware

## Virtual Lab

### Environment Variables
In order to get the slice of the Enterprise clusterm the following Environment varibale have to be defined

e.g.


### Build
./build.sh

or manually

docker build --build-arg CREDREDISPASSWORD --build-arg CREDREDISHOST --build-arg CREDREDISPORT -t redisuniversity/workshop-lab .

docker build -t redisuniversity/workshop-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/workshop-lab

### Tag
Need to change <version> to align to AVL version number
docker tag redisuniversity/workshop-lab gcr.io/redis-labs/workshop-lab:<version>

### Push
Push to Docker Hub
docker push redisuniversity/workshop-lab

###Push to GCR for AVL pull
docker push gcr.io/redis-labs/workshop-lab:<version>
