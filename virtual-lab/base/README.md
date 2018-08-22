# Build
docker build -t redislabs/virtual-lab .

# Run
docker run --rm --name redis-lab -p:8888:8888 redislabs/virtual-lab
