# ed-courseware

## Virtual Lab for RU201, RediSearch

### Data

You will need to prepare a data dump from a Redis instance with the data loaded in it and nothing else in there.

To do this, use the data loader which is contained and documented in the [RU201 GitHub repo](https://github.com/redislabs-training/ru201), then export an RDB file and place it in `dump/ru201.rdb`.  The Docker build process will expect to find it there and use it when building the container.

We don't keep this file in GitHub as it is over 100Mb in size.

### Build

```
./build.sh
```

or manually

docker build -t redislabs/ru201-lab .

As part of the build process, the contents of the [RU201 GitHub repo](https://github.com/redislabs-training/ru201) will be cloned into the `redisu` folder, which is git ignored.

### Run

```
./run.sh
```

or...

```
docker run --rm --name redis-lab -p:8888:8888 -v $PWD:/rdb redisuniversity/ru201-lab
```

### Push

```
./deploy.sh
```

Or manually...

Push to Docker Hub:

```
docker push redisuniversity/ru201-lab
```

## Build zip file

(**Note:** we no longer do this as this course now has its own [GitHub repo](https://github.com/redislabs-training/ru201))

From a running Virtual Lab, run the following:

```
cd /src
zip -r ru201.zip * -x *node_modules* -x redisu/ru201/data/General_Building_Permits.csv
cp ru201.zip /rdb/ru201.zip
```
