# ed-courseware

## Virtual Lab

### Build

```
./build.sh
```

or manually

```
docker build -t redisuniversity/redisconf-streams .
```

### Run

```
./run.sh
```

or

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-streams
```

### Tag

Need to change `<version>` to align to AVL version number.

```
docker tag redisuniversity/redisconf-streams gcr.io/redis-labs/redisconf-streams:<version>
```

### Push

Push to Docker Hub

```
docker push redisuniversity/redisconf-streams
```

###Push to GCR for AVL pull

```
docker push gcr.io/redis-labs/redisconf-streams:<version>
```

## Build zip file

From a running Virtual Lab, run the following
