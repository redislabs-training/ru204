# ed-courseware

## Virtual Lab

### Build

```
./build.sh
```

or manually

```
docker build -t redisuniversity/redisconf-redisearch .
```

### Run

```
./run.sh
```

or 

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-redisearch
```

### Tag
Need to change `<version>` to align to AVL version number.

```
docker tag redisuniversity/redisconf-redisearch gcr.io/redis-labs/redisconf-redisearch:<version>
```

### Push

Push to Docker Hub

```
docker push redisuniversity/redisconf-redisearch
```

###Push to GCR for AVL pull

```
docker push gcr.io/redis-labs/redisconf-redisearch:<version>
```

## Build zip file

From a running Virtual Lab, run the following
