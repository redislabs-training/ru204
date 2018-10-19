# ed-courseware

## Pylint
Run pylint on all code before release
```pylint -d bad-indentation --rcfile /src/.pylintrc /src/pth/to/file.py```

## Virtual Lab

### Build
./build.sh

or manually

docker build -t redislabs/ru201-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redislabs/ru201-lab

### Tag
Need to change <version> to align to AVL version number
docker tag redislabs/ru201-lab gcr.io/redis-labs/ru201-lab:<version>

### Push
Push to Docker Hub
docker push redislabs/ru201-lab

###Push to GCR for AVL pull
docker push gcr.io/redis-labs/ru201-lab:<version>