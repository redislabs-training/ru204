# ed-courseware

## Virtual Lab

### Build

```
./build.sh
```

or manually

```
docker build -t redisuniversity/redisconf-redisgraph .
```

### Run

```
./run.sh
```

or manually

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-redisgraph
```
### Tag

Need to change `<version>` to align to AVL version number

```
docker tag redisuniversity/redisconf-redisgraph gcr.io/redis-labs/redisconf-redisgraph:<version>
```

### Push

Push to Docker Hub

```
docker push redisuniversity/redisconf-redisgraph
```

###Push to GCR for AVL pull

```
docker push gcr.io/redis-labs/redisconf-redisgraph:<version>
```

## Build zip file

From a running Virtual Lab, run the following
