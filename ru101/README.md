# ed-courseware

## Pylint
Run pylint on all code before release
```pylint -d bad-indentation --rcfile /src/.pylintrc /src/pth/to/file.py```

## Virtual Lab

### Build
docker build -t redislabs/ru101-lab .

### Run
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redislabs/ru101-lab

### Tag
Need to change <version> to align to AVL version number
docker tag redislabs/ru101-lab gcr.io/redis-labs/ru101-lab:<version>

### Push
Push to Docker Hub
docker push redislabs/ru101-lab

Push to GCR for AVL pull
docker push gcr.io/redis-labs/ru101-lab:<version>
