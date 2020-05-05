# ed-courseware

## Virtual Lab

### Build

```
./build.sh
```

or manually

```
docker build -t redisuniversity/redisconf-redisbloom .
```

### Run

```
./run.sh
```

or manually

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-redisbloom
```

### Tag

Need to change `<version>` to align to AVL version number

```
docker tag redisuniversity/redisconf-redisbloom gcr.io/redis-labs/redisconf-redisbloom:<version>
```

### Push

Push to Docker Hub

```
docker push redisuniversity/redisconf-redisbloom
```

###Push to GCR for AVL pull

```
docker push gcr.io/redis-labs/redisconf-redisbloom:<version>
```

## Build zip file

From a running Virtual Lab, run the following
