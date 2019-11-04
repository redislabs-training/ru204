# ed-courseware

## Virtual Lab

### Build

```
./build.sh
```

or manually

```
docker build -t redisuniversity/redisconf-redisai .
```

### Run

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/redisconf-redisai
```

### Tag

Need to change `<version>` to align to AVL version number.

```
docker tag redisuniversity/redisconf-redisai gcr.io/redis-labs/redisconf-redisai:<version>
```

### Push
Push to Docker Hub

```
docker push redisuniversity/redisconf-redisai
```

Push to GCR for AVL pull

```
docker push gcr.io/redis-labs/redisconf-redisai:<version>
```


## Build zip file
From a running Virtual Lab, run the following
