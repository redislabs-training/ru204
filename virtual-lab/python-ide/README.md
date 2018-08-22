# Build
docker build -t redislabs/python-virtual-lab .

# Run
docker run --rm --name redis-lab -p:8888:8888 redislabs/python-virtual-lab